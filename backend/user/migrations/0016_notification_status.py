# Generated by Django 4.2.1 on 2023-12-28 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_alter_userprofile_verification_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.CharField(choices=[('PENDING', 'peding'), ('HANDLED', 'handled')], default='PENDING', max_length=10),
        ),
    ]