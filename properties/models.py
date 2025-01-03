from django.contrib.auth import get_user_model
from django.db import models

class Property(models.Model):
  TYPE_CHOICES = [
    ('apartment', 'شقة'),
    ('office', 'مكتب'),
    ('shop', 'محل'),
  ]
  name = models.CharField(max_length=100, verbose_name="اسم العقار")
  propert_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="نوع العقار")
  description = models.TextField(verbose_name="الوصف")
  address = models.TextField(verbose_name="العنوان")
  owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="المالك")

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = "عقار"
    verbose_name_plural = "العقارات"