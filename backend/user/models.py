from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(null=True, max_length=100)
    online = models.BooleanField(default=False)

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend_with = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)