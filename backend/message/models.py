from django.db import models
from channel.models import Channel, Member

MESSAGE_TYPE = (
    ("TEXT", "text"),
    ("IMAGE", "image")
)

class Message(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, related_name='messages', on_delete=models.CASCADE)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE, default="TEXT")
    content = models.TextField()
    reply = models.ForeignKey("Message", null=True, blank=True, on_delete=models.DO_NOTHING)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.channel.id}_{self.content}'

class Emoji(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    url = models.CharField(max_length=50)

class Reaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member)


