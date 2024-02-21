import json
import logging

logger = logging.getLogger(__name__)
from django.core.management.base import BaseCommand

from setting_ads.models import Bot, Channel_type, Channels, Client_Settings, KeywordChannelAds


# bot.json
# channel_type.json
# client.json
# channels.json
# keyword.json

def json_loader(filename):
    with open(f"client/management/commands/json/{filename}", "r") as file:
        return json.loads(file.read())


def add_data_to_db(data, model):
    for item in data:
        fields = item['fields']
        bot_token = fields.get('bot_token')
        if bot_token and not model.objects.filter(bot_token=bot_token).exists():
            model.objects.create(**fields)


def add_data_to_channel_db(data, model):
    for item in data:
        pk = item['pk']
        channel_name = item['fields'].get('channel_name')
        my_channel = item['fields'].get('my_channel')
        print("my_channel", pk, my_channel)
        bot = item['fields'].get('bot')
        type = item['fields'].get('type')
        channel_link = item['fields'].get('channel_link')
        channel_id = item['fields'].get('channel_id')
        type_obj = Channel_type.objects.get(pk=type)

        if not model.objects.filter(channel_id=channel_id).exists():
            if my_channel == False:
                print("my_channel", channel_id, my_channel)
                model.objects.create(
                    channel_name=channel_name,
                    channel_link=channel_link,
                    my_channel=my_channel,
                    channel_id=channel_id,
                    bot=bot,
                    type=type_obj)
            if my_channel == True:
                bot_obj = Bot.objects.get(pk=bot)
                print("my_channel", channel_id, my_channel)
                model.objects.create(
                    channel_name=channel_name,
                    channel_link=channel_link,
                    my_channel=my_channel,
                    channel_id=channel_id,
                    bot=bot_obj,
                    type=type_obj)

def channel_id_finder(channel_data,id):
    for item in channel_data:
        if item['pk'] == id:
            return item['fields']['channel_id']

def add_data_to_keyword_db(data, model):
    for item in data:
        fields = item['fields']
        channel = fields.get('channel')
        text = fields.get('text')

        channel_id = channel_id_finder(json_loader("channels.json"),channel)
        channel_obj= Channels.objects.get(channel_id=channel_id)
        if not model.objects.filter(text=text, channel=channel_obj).exists():
            model.objects.create(
                text=text,
                channel=channel_obj
            )

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            bot_data = json_loader("bot.json")
            channel_type_data = json_loader("channel_type.json")
            client_data = json_loader("client.json")
            channels_data = json_loader("channels.json")
            keyword_data = json_loader("keyword.json")

            add_data_to_db(bot_data, Bot)
            add_data_to_db(channel_type_data, Channel_type)
            add_data_to_db(client_data, Client_Settings)
            add_data_to_channel_db(channels_data, Channels)
            add_data_to_keyword_db(keyword_data, KeywordChannelAds)

            print("Data loaded successfully")
        except Exception as e:
            logger.exception("Error occurred while loading data")
            print("An error occurred while loading data. Please check logs for more details.")
