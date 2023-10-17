from django.db import models
from django.contrib.auth.models import User
from channel.models import Channel

NOTIFICATION_TYPE = (
    ("FRIEND_REQUEST", "friend_request"),
    ("FRIEND_ACCEPT", "friend_accept"),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    verification_code = models.CharField(null=True, max_length=10)
    bio = models.CharField(null=True, max_length=100)
    avatar_url = models.CharField(null=True, max_length=128)
    phone_number = models.CharField(null=True, max_length=15)
    address = models.CharField(null=True, max_length=100)
    online = models.BooleanField(default=False)

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend_with = models.ForeignKey(User, on_delete=models.CASCADE)

class Notification(models.Model):
    receiver = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)
    create_at = models.DateTimeField(auto_now_add=True)