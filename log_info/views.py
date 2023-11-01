from django.shortcuts import render

from setting_ads.models import Channels
from .models import Listening_channels, Message_log, SomeErrors


# Create your views here.


def listening_channels_view(channel_list: list):
    for channel in channel_list:
        if Channels.objects.filter(channel_id=channel).exists():
            channel = Channels.objects.get(channel_id=channel)
            try:
                Listening_channels.objects.get(channel_id=channel, channel=channel)
            except:
                try:
                    Listening_channels.objects.create(channel_id=channel, channel=channel)
                except Exception as e:
                    SomeErrors.objects.create(title='listening_channels', error=e)
        else:
            SomeErrors.objects.create(title='listening_channels', error=f"{channel} not found")


def message_log_view(message, log,is_sent=None):
    try:
        message = Message_log.objects.get(message=message)
        message.log = message.log + '\n' + 100 * '-' + f"\n{log}"
        if is_sent:
            message.is_sent=is_sent
        message.save()
    except:
        Message_log.objects.create(message=message, log=log)
