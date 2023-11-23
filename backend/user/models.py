from django.db import models
from django.contrib.auth.models import User
from channel.models import Channel
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from .utils import sendForgetPasswordEmail

NOTIFICATION_TYPE = (
    ("FRIEND_REQUEST", "friend_request"),
    ("FRIEND_ACCEPT", "friend_accept"),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    verification_code = models.CharField(null=True, max_length=10)
    bio = models.CharField(null=True, max_length=100)
    avatar_url = models.CharField(null=True, max_length=512)
    phone_number = models.CharField(null=True, max_length=15)
    address = models.CharField(null=True, max_length=100)
    online = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
    
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
        sendForgetPasswordEmail(reset_password_token)
    

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend_with = models.ForeignKey(User, on_delete=models.CASCADE)

class Notification(models.Model):
    receiver = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)
    create_at = models.DateTimeField(auto_now_add=True)