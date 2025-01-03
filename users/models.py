from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="رقم الهاتف")