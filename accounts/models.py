from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
  birth_date = models.DateField(verbose_name="تاريخ الميلاد", blank=True, null=True)
  bio = models.TextField(verbose_name="السيرة الذاتية", blank=True, null=True)

  def __str__(self):
    return self.username