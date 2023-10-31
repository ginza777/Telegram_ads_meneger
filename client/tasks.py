import datetime

from client.views import get_media_files_json_data
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from celery import Celery, shared_task

app = Celery('task', broker='redis://localhost:6379/0')


def send_msg(data: dict):
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
    if r.status_code == 400:
        print(
            f"400 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborilmadi   error: {r.json()} time: {current_time}")
    time.sleep(5)


def send_message(message_id):
    data_list = get_media_files_json_data(message_id)
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(send_msg, data_list)
        executor.shutdown(wait=True)
