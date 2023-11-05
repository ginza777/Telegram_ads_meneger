from django.db import models
from django.core.exceptions import ValidationError

from sender.sender import send_msg


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        db_table = 'timestamp'

class Client_Settings(TimeStamp):
    api_id = models.CharField(max_length=100,default='29441076')
    api_hash = models.CharField(max_length=100,default='2c170fe7bc8b8c8f8a1e1ad72db9710e')
    phone = models.CharField(max_length=100,default='+998993485501')
    token = models.CharField(max_length=100,null=True,blank=True)
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

class Channel_type(models.Model):
    type=models.CharField(max_length=100)

    def __str__(self):
        return self.type

class Channel_post_setting(models.Model):
    #new
    video=models.BooleanField(default=False)
    video_caption=models.BooleanField(default=False)
    photo=models.BooleanField(default=False)
    photo_caption=models.BooleanField(default=False)
    caption=models.BooleanField(default=False)
    text=models.BooleanField(default=False)


class Channels(TimeStamp):
    channel_name = models.CharField(max_length=250)
    channel_link = models.CharField(max_length=250)
    channel_id = models.CharField(max_length=100, unique=True)
    my_channel = models.BooleanField(default=False)
    bot = models.ForeignKey(Bot, on_delete=models.PROTECT, null=True, blank=True)
    type=models.ForeignKey(Channel_type,on_delete=models.PROTECT)
    setting=models.OneToOneField(Channel_post_setting,on_delete=models.CASCADE,null=True,blank=True)




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
        if self.my_channel and self.bot is None:
            raise ValidationError('This channel is my channel, please select bot')
        if not self.my_channel:
            self.bot = None
        if self.my_channel and self.bot is not None:
            res=send_msg('Hello', self.bot.bot_token, self.channel_id)
            if not res:
                raise ValidationError('This bot did not send message to this channel')
        if self.type is None:
            raise ValidationError('Please select channel type')

        if not self.channel_link.startswith('https://t.me/'):
            raise(ValidationError('Please enter valid channel link'))




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


