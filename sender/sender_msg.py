import datetime

from django.utils import timezone

from client.models import Message, Message_history
from setting_ads.models import Channels
from .views import get_media_files_json_data
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from celery import Celery, shared_task
from log_info.views import message_log_view, message_sent_status


def send_msg(data):
    message = Message.objects.get(message_id=data['message_id'])
    url = f"https://api.telegram.org/bot{data['token']}/sendMediaGroup"
    # Fayllarni to'g'ri ko'rsatish uchun
    files = {key: (f"file{index}", file, 'application/octet-stream') for index, (key, file) in
             enumerate(data['files'].items())}

    r = requests.post(url, data=data['data'], files=files)
    current_time = datetime.datetime.fromtimestamp(time.time())

    channel_from = Channels.objects.get(channel_id=data['channel_from'])
    channel_to = Channels.objects.get(channel_id=data['data']['chat_id'])
    type = channel_from.type

    if r.status_code == 200:
        message_sent_status(message=message, status=True, channel_from=channel_from, channel_to=channel_to, type=type)

        print(
            f"200 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborildi  yuborildi time: {current_time}"
        )
        message_log_view(message,
                         f"200 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborildi  yuborildi time: {current_time}",
                         is_sent=True)
        message.send_status = True
        message.save()
        time.sleep(2)

    if r.status_code == 400:
        message_sent_status(message=message, status=False, channel_from=channel_from, channel_to=channel_to, type=type)
        print(
            f"400 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborilmadi   error: {r.json()} time: {current_time}")
        message_log_view(message,
                         f"400 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborilmadi   error: {r.json()} time: {current_time}")
        time.sleep(2)

    time.sleep(1)


def send_message(message_id):
    data_list = get_media_files_json_data(message_id)
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(send_msg, data_list)
        executor.shutdown(wait=True)
