from django.db import models
from users.models import User
# Create your models here.

class Channel(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    title = models.CharField(max_length=200)
    member_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Member(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    channel_id = models.ForeignKey(Channel, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=200)
    role = models.CharField(max_length=200, choices=(
        ('creator', 'Creator'),
        ('admin', 'Admin'),
        ('member', 'Member')
    ))