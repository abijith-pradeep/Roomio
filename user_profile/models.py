from django.db import models

from login.models import User

class Pet(models.Model):
    pet_name = models.CharField(max_length=50)
    pet_type = models.CharField(max_length=50)
    pet_size = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')

    class Meta:
        unique_together = ('pet_name', 'pet_type', 'owner')
