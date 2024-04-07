from django.db import models

from login.models import User

class Pet(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'type', 'owner')
