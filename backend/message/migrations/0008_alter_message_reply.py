# Generated by Django 4.2.6 on 2023-10-16 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0007_alter_message_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='message.message'),
        ),
    ]
