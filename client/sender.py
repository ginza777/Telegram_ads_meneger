import requests

from .views import *
from client import models



def send_media_group(message_id):
    channel_id = models.Message.objects.get(message_id=message_id).channel_from
    token=models.Channel_config.objects.get(from_channel__channel_id=channel_id).bot.bot_token
    print(message_id)
    print(token)
    print(models.Message.objects.get(message_id=message_id).channel_from)
    url = f'https://api.telegram.org/bot{token}/sendMediaGroup'
    data, files = get_media_files_json_data(message_id)
    print(100 * '-')
    print(data)
    print(files)
    r = requests.post(url, data=data, files=files)
    print(r.status_code)
    print(r.json())
    if r.status_code == 200:
        return True
    else:
        return False


def send_msg(message, token, channel_id):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {
        'chat_id': channel_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        return False, r.status_code
    else:
        return True, r.status_code


def send_as_photo(image_caption, image, token, channel_id):
    url = f'https://api.telegram.org/bot{token}/sendPhoto'
    params = {
        'chat_id': channel_id,
        'caption': image_caption,
        'parse_mode': 'HTML',
        'photo': image,
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        return False, r.status_code
    else:
        return True, r.status_code
