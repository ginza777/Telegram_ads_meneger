from django.db import models
from django.core.exceptions import ValidationError

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
    bot_token = models.CharField(max_length=100, unique=True)
    bot_link = models.CharField(max_length=100)

    def __str__(self):
        return self.bot_name

    class Meta:
        db_table = 'bot_settings'


class Channels(TimeStamp):
    channel_name = models.CharField(max_length=250)
    channel_link = models.CharField(max_length=250)
    channel_id = models.CharField(max_length=100, unique=True)
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
        unique_together = ('text', 'channel')

    def clean(self):
        if self.channel.my_channel and KeywordChannelAds.objects.filter(channel=self.channel).exclude(
                id=self.id).exists():
            raise ValidationError('This channel already has keyword')


class Channel_config(TimeStamp):
    title = models.CharField(max_length=100)
    from_channel = models.ForeignKey(Channels, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='from_channel_configs', limit_choices_to={'my_channel': False},unique=True)
    to_channel = models.ForeignKey(Channels, on_delete=models.SET_NULL, null=True, related_name='to_channel_configs',
                                   limit_choices_to={'my_channel': True})
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
