from celery import Celery, shared_task
import requests

from client.views import get_media_files_json_data
import time
# Create a Celery instance
app = Celery('task', broker='redis://localhost:6379/0')

import logging

# Decorate the function with `shared_task`, not `@app_task`

import requests
import time

import requests
import time
from concurrent.futures import ThreadPoolExecutor

def send_msg(data: dict):
    url = f"https://api.telegram.org/bot{data['token']}/sendMediaGroup"
    print(100 * '*')
    print(data['token'])

    # Fayllarni to'g'ri ko'rsatish uchun
    files = {key: (f"file{index}", file, 'application/octet-stream') for index, (key, file) in enumerate(data['files'].items())}

    r = requests.post(url, data=data['data'], files=files)
    print(r.status_code)
    if r.status_code == 400:
        print(r.json())
    time.sleep(3)

def send_message(message_id):
    data_list = get_media_files_json_data(message_id)
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(send_msg, data_list)
        executor.shutdown(wait=True)

# send_msg2() ni olib tashlang, u shunday ko'p ishlatilmaydi




    # Ensure that data is serializable by converting non-serializable parts
    # to serializable formats. For example, if data['buffer'] is a BufferedReader,
    # you may convert it to a string or bytes.
    # data['buffer'] = data['buffer'].read()  # Convert to bytes, assuming it's binary data
    #
    # # Continue with your existing code to send the message
    # url = f"https://api.telegram.org/bot{data['token']}/sendMediaGroup"
    # r = requests.post(url, data=data['data'], files=data['files'])
    # print(100 * '*')
    # print(r.status_code)
    # print(data['data'])
    # print(data['files'])