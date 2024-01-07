from django.contrib import admin

from log_info.models import SomeErrors
from setting_ads.models import Channels
from .models import Filename, Message,Message_history


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
            channel_name = obj.channel_from.channel_name
        except:
            channel_name = None
            SomeErrors.objects.create(title=f"Admin panelda channel_from_name error",
                                      error=f"channel_name={channel_name}\n message={obj.message_id} \n id={obj.id}")
        return channel_name

    def channel_to_count(self, obj):
        try:
            channel_to_count = Channels.objects.filter(type=obj.channel_from.type, my_channel=True).count()
        except:
            channel_to_count = None
            SomeErrors.objects.create(title=f"Admin panelda channel_to_count error",
                                      error=f"channel_to_count={channel_to_count}\n message={obj.message_id} \n id={obj.id}")
        return channel_to_count

    list_filter = ( 'delete_status', 'send_status', 'end')
    #search filter
    search_fields = ('message_id', 'caption', 'photo', 'channel_from_name', 'channel_to_count', 'delete_status', 'single_photo', 'send_status',)

@admin.register(Message_history)
class Message_historyAdmin(admin.ModelAdmin):
    list_display = ('message', 'from_channel', 'to_channel', 'type', 'sent_status', 'time', 'created_at', 'updated_at')
    search_fields = ('message', 'from_channel', 'to_channel', 'type', 'sent_status', 'time')
    list_filter = ('from_channel', 'to_channel', 'type', 'sent_status', 'time')