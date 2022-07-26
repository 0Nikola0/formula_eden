from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Poraka(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender',  default=1)
    # global chat ke e nema potreba od receiver
    # receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender}: {self.message}"
    

    def get_text(self):
        return self.message

    def get_username(self):
        return self.sender.username

    class Meta:
        ordering = ('timestamp',)
