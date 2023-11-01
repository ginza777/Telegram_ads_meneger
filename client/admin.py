from django.contrib import admin

from log_info.models import SomeErrors
from setting_ads.models import Channel_config
from .models import Filename, Message


@admin.register(Filename)
class FilenameAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_id', 'filename', 'is_caption', 'is_photo', 'created_at', 'updated_at')
    search_fields = ('message_id', 'filename')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
    'message_id', 'caption', 'photo', 'channel_from_name', 'channel_to', 'delete_status', 'single_photo', 'send_status',
    'photo_count', 'end', 'updated_at')

    def channel_from_name(self, obj):
        try:
            channel_name = Channel_config.objects.get(
                from_channel__channel_id=str(obj.channel_from)).from_channel.channel_name
        except:
            channel_name = None
            SomeErrors.objects.create(title=f"Admin panelda channel_from_name error",
                                      error=f"channel_name={channel_name}\n message={obj.message_id} \n id={obj.id}")
        return channel_name

    def channel_to(self, obj):
        try:
            channel_name = Channel_config.objects.get(
                to_channel__channel_id=str(obj.channel_from)).to_channel.channel_name
        except:
            channel_name = None
            SomeErrors.objects.create(title=f"Admin panelda channel_to error",
                                      error=f"channel_name={channel_name}\nmmessage={obj.message_id}\nid={obj.id}")
        return channel_name
