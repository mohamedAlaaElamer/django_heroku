from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Chatmessage(models.Model):
    formuser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sentmessage")
    touser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="indoxmessage")
    message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-id']
