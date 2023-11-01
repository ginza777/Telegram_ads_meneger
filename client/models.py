from django.db import models

from setting_ads.models import Channels


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        db_table = 'timestamp'


class Filename(TimeStamp):
    message_id = models.CharField(max_length=50)
    filename = models.CharField(max_length=100)
    is_caption = models.BooleanField(default=False)
    is_photo = models.BooleanField(default=False)

    def __str__(self):
        return self.filename

    class Meta:
        db_table = 'filename'


class Message(TimeStamp):
    message_id = models.CharField(max_length=500, unique=True)
    caption = models.BooleanField(default=False)
    photo = models.BooleanField(default=False)
    channel_from = models.ForeignKey(Channels, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='from_channel_messages', limit_choices_to={'my_channel': False})
    delete_status = models.BooleanField(default=True)
    single_photo = models.BooleanField(default=False)
    send_status = models.BooleanField(default=False)
    photo_count = models.IntegerField(default=0)
    ready = models.BooleanField(default=False)
    end = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.caption and self.photo:
            self.delete_status = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.message_id

    class Meta:
        db_table = 'message'
