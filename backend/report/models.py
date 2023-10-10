from django.db import models
from django.contrib.auth.models import User
from channel.models import Channel

REPORT_TYPE = (
    ("REPORT_USER", "report_user"),
    ("REPORT_CHANNEL", "report_channel")
)

class Report(models.Model):
    reporter = models.ForeignKey(User, related_name='reporters', on_delete=models.DO_NOTHING)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE)
    reported_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reported_channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING)
    reason = models.TextField()
    processed = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)