# Generated by Django 4.2.1 on 2023-11-30 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='verification_code',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]