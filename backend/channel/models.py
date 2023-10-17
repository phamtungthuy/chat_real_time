from django.db import models
from django.contrib.auth.models import User

ROLES = (
    ("MEMBER", "Thành viên"),
    ("CREATOR", "Trưởng nhóm")
)

class Channel(models.Model):
    title = models.CharField(max_length=30)
    avatar_url = models.CharField(null=True, max_length=128)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}_{self.title}'

class Member(models.Model):
    user = models.ForeignKey(User, related_name='members', on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, related_name='members', on_delete=models.CASCADE)
    nickname = models.CharField(blank=True, null=True, max_length=30)
    role = models.CharField(max_length=10, default="MEMBER", choices=ROLES)

    def __str__(self):
        return f'{self.user}_{self.channel.title}'
