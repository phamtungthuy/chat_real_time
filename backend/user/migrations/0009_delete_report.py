# Generated by Django 4.2.4 on 2023-10-10 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_userprofile_verification_code_report'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Report',
        ),
    ]
