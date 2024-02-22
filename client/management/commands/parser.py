import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from setting_ads.models import Bot
def get_info(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.post(url)
    print(response.json())
    return response.json().get("result").get("username"), response.json().get("result").get("first_name")


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
        print("bot_token: ", bot_token)
        get_info(bot_token)
        chat_id = -1002041724232
        r=send_to_telegram(bot_token, chat_id)
        print("res:: ", r)

