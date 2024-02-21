import json
from django.core.serializers import serialize
from django.http import JsonResponse
from setting_ads.models import Channels, Client_Settings, Bot, Channel_type, Channel_post_setting, KeywordChannelAds
from django.shortcuts import render
def channels_to_json(request):
    channels = Channels.objects.all()
    channels_data = serialize('json', channels)
    return JsonResponse(json.loads(channels_data), safe=False)

def client_settings_to_json(request):
    client=Client_Settings.objects.all()
    client_data = serialize('json', client)
    return JsonResponse(json.loads(client_data), safe=False)


def bot_to_json(request):
    bot = Bot.objects.all()
    bot_data = serialize('json', bot)
    return JsonResponse(json.loads(bot_data), safe=False)


def channel_type_to_json(request):
    channel_type = Channel_type.objects.all()
    channel_type_data = serialize('json', channel_type)
    return JsonResponse(json.loads(channel_type_data), safe=False)


def channel_post_setting_to_json(request):
    channel_post_setting = Channel_post_setting.objects.all()
    channel_post_setting_data = serialize('json', channel_post_setting)
    return JsonResponse(json.loads(channel_post_setting_data), safe=False)


# Path: urls.py
def keyword_channel_ads_to_json(request):
    keyword_channel_ads = KeywordChannelAds.objects.all()
    keyword_channel_ads_data = serialize('json', keyword_channel_ads)
    return JsonResponse(json.loads(keyword_channel_ads_data), safe=False)




def all_url_list_html(request):
    url = 'https://sherzamon.cloud'
    context = {
        'channels': f'{url}/channels/json/',
        'client_settings': f'{url}/client_settings/json/',
        'bot': f'{url}/bot/json/',
        'channel_type': f'{url}/channel_type/json/',
        'keyword_channel_ads': f'{url}/keyword/json/',
    }
    return render(request, 'index.html', context)
