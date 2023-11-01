from django.db import models
from setting_ads.models import Channels,Client_Settings
from client.models import Message
# Create your models here.


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
        db_table = 'timestamp'

class Message_log(TimeStamp):
    message=models.ForeignKey(Message,on_delete=models.CASCADE,related_name='message_log',null=True,blank=True)
    log=models.TextField()
    is_sent=models.BooleanField(default=False)
    class Meta:
        db_table = 'message_log'
        verbose_name_plural = 'Message_log'


class Listening_channels(TimeStamp):
    channel_id = models.CharField(max_length=255, unique=True)
    listening_channel = models.ForeignKey(Channels, on_delete=models.SET_NULL, related_name='listening_channels',
                                          null=True, blank=True)

    class Meta:
        db_table = 'listening_channels'
        verbose_name_plural = 'listening_channels'
        unique_together = ('channel_id', 'listening_channel')

    def __str__(self):
        return f"{self.channel_id}"

class Note(TimeStamp):
    title=models.CharField(max_length=255)
    note=models.TextField()
    class Meta:
        db_table = 'note'
        verbose_name_plural = 'note'

    def __str__(self):
        return self.title

class SomeErrors(TimeStamp):
    title=models.CharField(max_length=255)
    error=models.TextField()
    class Meta:
        db_table = 'some_errors'
        verbose_name_plural = 'some_errors'

    def __str__(self):
        return self.title