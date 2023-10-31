from django.core.exceptions import ValidationError
from django.db import models

from client.sender import send_media_group


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        db_table = 'timestamp'


class Client_Settings(TimeStamp):
    api_id = models.CharField(max_length=100)
    api_hash = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    session = models.FileField(upload_to='session', null=True, blank=True)

    def __str__(self):
        return self.phone

    class Meta:
        db_table = 'client_settings'

    def save(self, *args, **kwargs):
        if self.session:
            self.session.name = str(self.phone) + '.session'
        super().save(*args, **kwargs)


class Bot(TimeStamp):
    bot_name = models.CharField(max_length=100)
    bot_token = models.CharField(max_length=100,unique=True)
    bot_link = models.CharField(max_length=100)

    def __str__(self):
        return self.bot_name

    class Meta:
        db_table = 'bot'



class Channels(TimeStamp):
    channel_name = models.CharField(max_length=250)
    channel_link = models.CharField(max_length=250)
    channel_id = models.CharField(max_length=100)
    my_channel = models.BooleanField(default=False)

    def __str__(self):
        return self.channel_name

    class Meta:
        db_table = 'channels'
        unique_together = ('channel_id', 'my_channel')

    def save(self, *args, **kwargs):
        if not self.channel_id.startswith('-'):
            if self.channel_id.startswith('100'):
                self.channel_id = '-' + self.channel_id
            else:
                self.channel_id = '-100' + self.channel_id
        super().save(*args, **kwargs)

    def clean(self):
        if Channels.objects.filter(channel_id=self.channel_id).exclude(id=self.id).exists():
            raise ValidationError('This channel_id already exists')


class KeywordChannelAds(TimeStamp):
    text = models.TextField()
    channel = models.ForeignKey(Channels, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'keywordchannelads'

    def clean(self):
        if self.channel.my_channel and KeywordChannelAds.objects.filter(channel=self.channel).exclude(
                id=self.id).exists():
            raise ValidationError('This channel already has keyword')


class Channel_config(TimeStamp):
    title = models.CharField(max_length=100)
    from_channel = models.ForeignKey(Channels, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='from_channel_configs', limit_choices_to={'my_channel': False})
    to_channel = models.ForeignKey(Channels, on_delete=models.SET_NULL, null=True, related_name='to_channel_configs',limit_choices_to={'my_channel': True})
    bot = models.ForeignKey(Bot, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'channel_config'
        unique_together = ('from_channel', 'to_channel')

    def clean(self):
        if self.from_channel.my_channel:
            raise ValidationError('This channel is my channel')
        if not self.to_channel.my_channel:
            raise ValidationError('This channel is not my channel')


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
    channel_from = models.CharField(max_length=100)
    delete_status = models.BooleanField(default=True)
    single_photo = models.BooleanField(default=False)
    send_status = models.BooleanField(default=False)
    photo_count = models.IntegerField(default=0)
    end = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.caption and self.photo:
            self.delete_status = False
        else:
            self.delete_status = True
        if self.photo_count > 1:
            self.single_photo = False
        if self.end and not self.delete_status:
            send_media_group(self.message_id)
            self.send_status = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.message_id

    class Meta:
        db_table = 'message'

