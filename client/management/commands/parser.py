import asyncio
from django.core.management.base import BaseCommand
from django.utils import timezone

from client.models import Filename
from setting_ads.models import Channels
from setting_ads.models import Client_Settings
import requests


def send_to_telegram(bot_token, chat_id):
    caption= f"Ads_manager Date: {timezone.now()}"
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    files = {'document': open("./mydatabase.sqlite3", 'rb')}
    data = {'chat_id': chat_id, 'caption': caption} if caption else {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    return response.json()


class Command(BaseCommand):

    def handle(self, *args, **options):
        help = 'Starts the Telegram listener'
        bot_token = "6607374521:AAHjnBaqbDqJKvFkF_HsiJ6losu50j6vHiE"
        chat_id = -1002041724232
        send_to_telegram(bot_token, chat_id)




