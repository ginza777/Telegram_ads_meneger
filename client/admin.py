from django.contrib import admin

from log_info.models import SomeErrors
from setting_ads.models import Channel_config, Channels
from .models import Filename, Message


@admin.register(Filename)
class FilenameAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_id', 'filename', 'is_caption', 'is_photo', 'created_at', 'updated_at')
    search_fields = ('message_id', 'filename')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
    'message_id', 'caption', 'photo', 'channel_from_name', 'channel_to_count', 'delete_status', 'single_photo', 'send_status',
    'photo_count', 'end', 'updated_at')

    def channel_from_name(self, obj):
        try:
            channel_name = Channels.objects.get(channel_id=str(obj.channel_from)).channel_name
        except:
            channel_name = None
            SomeErrors.objects.create(title=f"Admin panelda channel_from_name error",
                                      error=f"channel_name={channel_name}\n message={obj.message_id} \n id={obj.id}")
        return channel_name

    def channel_to_count(self, obj):
        try:
            channel_count = Channel_config.objects.filter(
                to_channel__channel_id=str(obj.channel_from)).count()
        except:
            channel_count = None
            SomeErrors.objects.create(title=f"Admin panelda channel_to error",
                                      error=f"channel_name={channel_count}\nmmessage={obj.message_id}\nid={obj.id}")
        return channel_count
