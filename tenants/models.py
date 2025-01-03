from django.db import models

class Tenant(models.Model):
  name = models.CharField(max_length=200, verbose_name="الاسم")
  phone = models.CharField(max_length=15, verbose_name="رقم الهاتف")
  email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
  address = models.TextField(verbose_name="العنوان")

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = "مستأجر"
    verbose_name_plural = "المستأجرون"