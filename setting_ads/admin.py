from django.contrib import admin
from .models import Client_Settings, Bot, Channels, KeywordChannelAds, Channel_type, Channel_post_setting

# Register your models here.

admin.site.register(Client_Settings)
@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('id', 'bot_name', 'bot_token', 'bot_link', 'created_at', 'updated_at')


#inline for channels vs KeywordChannelAds

class KeywordChannelAdsInline(admin.TabularInline):
    model = KeywordChannelAds
    extra = 2

@admin.register(Channel_post_setting)
class Channel_post_settingAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'video_caption', 'photo', 'photo_caption', 'caption', 'text')

@admin.register(Channels)
class ChannelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel_name', 'channel_link', 'channel_id', 'my_channel', 'type', 'updated_at')
    inlines = [KeywordChannelAdsInline]
    list_filter = ['my_channel', 'type']


@admin.register(KeywordChannelAds)
class KeywordChannelAdsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'channel', 'created_at', 'updated_at')
    list_filter = [ 'channel__type']

admin.site.register(Channel_type)

