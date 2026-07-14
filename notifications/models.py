from django.db import models

class Sender(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Notification(models.Model):

    CHANNEL_CHOICES=[("email", "Email"),("sms", "SMS"),("push", "Push"),]

    title = models.CharField(max_length=255)
    message = models.TextField()
    channel = models.CharField(max_length=10,choices= CHANNEL_CHOICES)
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE, related_name="notifications")

    def __str__(self):
        return self.title