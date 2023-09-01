from django.db import models
from chatChannels.models import Member, Channel
# Create your models here.
class Message(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    channel_id = models.ForeignKey(Channel, on_delete=models.CASCADE)
    content = models.TextField()
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)