from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
  phone = models.CharField(max_length=15, verbose_name="رقم الهاتف", blank=True, null=True)
  address = models.TextField(verbose_name="العنوان", blank=True, null=True)

  class Meta:
    permissions = [
      ("can_view_dashboard", "Can view dashboard"),
    ]

  def __str__(self):
    return self.username