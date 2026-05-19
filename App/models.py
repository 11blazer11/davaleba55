import uuid
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)


class Task(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title