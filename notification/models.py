from django.db import models
from tweets.models import Tweet
from django.contrib.auth.models import User
# Create your models here.


class Notification(models.Model):
    tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name="tweetaction")
    byuser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="useraction")
    action = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-id']
