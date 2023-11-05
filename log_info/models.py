from django.db import models
from setting_ads.models import Channels, Client_Settings, TimeStamp
from client.models import Message
# Create your models here.




class Message_log(TimeStamp):
    message=models.ForeignKey(Message,on_delete=models.CASCADE,related_name='message_log',null=True,blank=True)
    log=models.TextField()
    is_sent=models.BooleanField(default=False)
    class Meta:
        db_table = 'message_log'
        verbose_name_plural = 'Message_log'


class Listening_channels(TimeStamp):
    listening_channel = models.OneToOneField(Channels, on_delete=models.CASCADE, related_name='listening_channel',null=True,blank=True)


    class Meta:
        db_table = 'listening_channels'
        verbose_name_plural = 'listening_channels'


    def __str__(self):
        return f"{self.listening_channel}"

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