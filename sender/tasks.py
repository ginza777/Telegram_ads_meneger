import datetime

from client.models import Message, Message_sent_status
from setting_ads.models import Channels
from .views import get_media_files_json_data
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from celery import Celery, shared_task
from log_info.views import message_log_view
app = Celery('task', broker='redis://localhost:6379/0')


def send_msg(data: dict):
    message=Message.objects.get(id=data['message_id'])
    url = f"https://api.telegram.org/bot{data['token']}/sendMediaGroup"
    # Fayllarni to'g'ri ko'rsatish uchun
    files = {key: (f"file{index}", file, 'application/octet-stream') for index, (key, file) in
             enumerate(data['files'].items())}

    r = requests.post(url, data=data['data'], files=files)
    current_time = datetime.datetime.fromtimestamp(time.time())
    if r.status_code == 200:
        print(
            f"200 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborildi  yuborildi time: {current_time}"
        )
        message_log_view(message, f"200 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborildi  yuborildi time: {current_time}",is_sent=True)
        Message_sent_status.objects.create(
            message=message,
            from_channel=Channels.objects.get(channel_id=data['channel_from']),
            to_channel=Channels.objects.get(channel_id=data['data']['chat_id']),
            is_sent=True
        ).save()

    if r.status_code == 400:
        print(
            f"400 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborilmadi   error: {r.json()} time: {current_time}")
        message_log_view(message, f"400 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborilmadi   error: {r.json()} time: {current_time}")
        Message_sent_status.objects.create(
            message=message,
            from_channel=Channels.objects.get(channel_id=data['channel_from']),
            to_channel=Channels.objects.get(channel_id=data['data']['chat_id']),
            is_sent=False
        ).save()

def send_message(message_id):
    data_list = get_media_files_json_data(message_id)
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(send_msg, data_list)
        executor.shutdown(wait=True)
