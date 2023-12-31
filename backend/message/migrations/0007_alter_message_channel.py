# Generated by Django 4.2.4 on 2023-10-06 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0008_channel_avatar_url'),
        ('message', '0006_message_message_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='channel.channel'),
        ),
    ]
