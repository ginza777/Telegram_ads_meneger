# Generated by Django 4.2.6 on 2023-11-03 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setting_ads', '0001_initial'),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message_history',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='setting_ads.channel_type'),
        ),
    ]