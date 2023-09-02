from django.db import models
from django.contrib.auth.models import User

ROLES = (
    ("MEMBER", "Thành viên"),
    ("ADMIN", "Quản trị viên"),
    ("CREATOR", "Người lập nhóm")
)

class Channel(models.Model):
    title = models.CharField(max_length=30)
    memberCount = models.IntegerField()
    create_at = models.DateTimeField(auto_now=True)

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)
    role = models.CharField(max_length=10, default="MEMBER", choices=ROLES)
