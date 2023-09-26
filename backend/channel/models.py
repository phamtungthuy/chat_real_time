from django.db import models
from django.contrib.auth.models import User

ROLES = (
    ("MEMBER", "Thành viên"),
    ("ADMIN", "Quản trị viên"),
    ("CREATOR", "Người lập nhóm")
)

class Channel(models.Model):
    title = models.CharField(max_length=30)
    memberCount = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, related_name='members', on_delete=models.CASCADE)
    nickname = models.CharField(blank=True, null=True, max_length=30)
    role = models.CharField(max_length=10, default="MEMBER", choices=ROLES)

    def __str__(self):
        return str(self.user) + " - " + str(self.channel)
