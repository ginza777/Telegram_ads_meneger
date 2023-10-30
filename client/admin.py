from django.contrib import admin
from .models import Client_Settings, Bot, Channels, KeywordChannelAds, Channel_config, Filename, Message

admin.site.register(Client_Settings)
@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('id', 'bot_name', 'bot_token', 'bot_link', 'created_at', 'updated_at')

@admin.register(Channels)
class ChannelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel_name', 'channel_link', 'channel_id', 'my_channel', 'created_at', 'updated_at')

@admin.register(KeywordChannelAds)
class KeywordChannelAdsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'channel', 'created_at', 'updated_at')

@admin.register(Channel_config)
class ChannelConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'from_channel', 'to_channel', 'bot', 'created_at', 'updated_at')

@admin.register(Filename)
class FilenameAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_id', 'filename', 'is_caption', 'is_photo', 'created_at', 'updated_at')
    search_fields = ('message_id', 'filename')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_id', 'caption', 'photo', 'channel_from', 'delete_status', 'single_photo', 'send_status', 'photo_count', 'end', 'created_at', 'updated_at')
