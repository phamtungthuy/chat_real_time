# Generated by Django 4.2.4 on 2023-09-29 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0004_alter_member_channel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='memberCount',
        ),
        migrations.AlterField(
            model_name='member',
            name='nickname',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
