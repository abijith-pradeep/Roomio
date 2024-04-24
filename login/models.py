from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    dob = models.DateField()
    gender = models.PositiveSmallIntegerField()  
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    # password is already created and automatically Hashed because of AbstractUser

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
