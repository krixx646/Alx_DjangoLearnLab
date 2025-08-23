from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    actor = models.ForeignKey(User, related_name="actions", on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)  # e.g. "liked", "commented on"

    # Generic foreign key setup
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # stores the model
    object_id = models.PositiveIntegerField()  # stores the object’s PK
    target = GenericForeignKey("content_type", "object_id")  # combines them

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target} for {self.recipient}"