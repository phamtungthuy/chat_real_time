# Generated by Django 4.2.4 on 2023-10-02 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0007_alter_member_nickname_alter_member_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='avatar_url',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
