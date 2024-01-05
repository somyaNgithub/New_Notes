from django.db import models
import uuid

# Create your models here.

class CustomUser(models.Model):
    U_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userName = models.CharField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.userName


