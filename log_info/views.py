from django.shortcuts import render
from django.utils import timezone

from client.models import Message_history
from setting_ads.models import Channels
from .models import Listening_channels, Message_log, SomeErrors


# Create your views here.


def listening_channels_view(channel_list: list):
    for channel_link in channel_list:
        if Channels.objects.filter(channel_link=channel_link).exists():
            channel = Channels.objects.get(channel_link=channel_link)
            try:
                Listening_channels.objects.get(listening_channel=channel)
            except:
                try:
                    Listening_channels.objects.create(listening_channel=channel)
                except Exception as e:
                    SomeErrors.objects.create(title='listening_channels', error=e)
        else:
            SomeErrors.objects.create(title='listening_channels', error=f"{channel_link} not found")

def message_log_view(message, log, is_sent=False):
    try:
        message_log_instance = Message_log.objects.get(message=message)
        message_log_instance.log += '\n' + 100 * '-' + f"\n{log}"
        if is_sent is not None:
            message_log_instance.is_sent = is_sent
        message_log_instance.save()
    except Message_log.DoesNotExist:
        Message_log.objects.create(message=message, log=log, is_sent=is_sent)


def message_sent_status(message=None,status=False,channel_from=None,channel_to=None,type=None):
    try:
        message = Message_history.objects.get(message=message,from_channel=channel_from,to_channel=channel_to,type=type)
        message.sent_status = status
        message.time = timezone.now()
        message.save()
    except:
        Message_history.objects.create(message=message, sent_status=status,from_channel=channel_from,to_channel=channel_to,type=type)


