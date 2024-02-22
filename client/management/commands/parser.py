import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from setting_ads.models import Bot


def send_to_telegram(bot_token, chat_id):
    caption = f"Ads_manager Date: {timezone.now()}"
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    files = {'document': open("./mydatabase.sqlite3", 'rb')}
    data = {'chat_id': chat_id, 'caption': caption} if caption else {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    return response.json()


class Command(BaseCommand):

    def handle(self, *args, **options):
        help = 'Starts the Telegram listener'
        if Bot.objects.all().count() > 0:
            bot_token = Bot.objects.last().bot_token
        else:
            bot_token = "6567332198:AAHRaGT5xLJdsJbWkugqgSJHbPGi8Zr2_ZI"
        chat_id = -1002041724232
        send_to_telegram(bot_token, chat_id)
        print("done")
