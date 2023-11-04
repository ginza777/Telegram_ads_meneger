# Generated by Django 4.2.6 on 2023-11-03 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bot_name', models.CharField(max_length=100)),
                ('bot_token', models.CharField(max_length=100, unique=True)),
                ('bot_link', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'bot_settings',
            },
        ),
        migrations.CreateModel(
            name='Channel_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Channels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('channel_name', models.CharField(max_length=250)),
                ('channel_link', models.CharField(max_length=250)),
                ('channel_id', models.CharField(max_length=100, unique=True)),
                ('my_channel', models.BooleanField(default=False)),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='setting_ads.bot')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='setting_ads.channel_type')),
            ],
            options={
                'db_table': 'channels',
                'unique_together': {('channel_id', 'my_channel')},
            },
        ),
        migrations.CreateModel(
            name='Client_Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('api_id', models.CharField(default='29441076', max_length=100)),
                ('api_hash', models.CharField(default='2c170fe7bc8b8c8f8a1e1ad72db9710e', max_length=100)),
                ('phone', models.CharField(default='+998993485501', max_length=100)),
                ('token', models.CharField(blank=True, max_length=100, null=True)),
                ('session', models.FileField(blank=True, null=True, upload_to='session')),
            ],
            options={
                'db_table': 'client_settings',
            },
        ),
        migrations.CreateModel(
            name='KeywordChannelAds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setting_ads.channels')),
            ],
            options={
                'db_table': 'keywordchannelads',
                'unique_together': {('text', 'channel')},
            },
        ),
    ]