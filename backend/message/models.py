from django.db import models
from channel.models import Channel, Member

class Message(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    content = models.TextField()
    reply = models.ForeignKey("Message", null=True, on_delete=models.DO_NOTHING)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

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


