from django.contrib import admin
from .models import Message_log, Listening_channels, Note, SomeErrors

@admin.register(Message_log)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ['message','is_sent', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['message__text']  # Assuming 'text' is a field in the Message model

@admin.register(Listening_channels)
class ListeningChannelsAdmin(admin.ModelAdmin):
    list_display = ['id', 'listening_channel', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['channel_id']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['title']

@admin.register(SomeErrors)
class SomeErrorsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['title']
