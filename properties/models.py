from django.db import models


class Property(models.Model):
  PROPERTY_TYPES = [
    ('residential', 'سكني'),
    ('commercial', 'تجاري'),
  ]

  name = models.CharField(max_length=255, verbose_name="اسم الوحدة")
  type = models.CharField(max_length=50, choices=PROPERTY_TYPES, verbose_name="نوع الوحدة")
  area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المساحة")
  price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
  occupied = models.BooleanField(default=False, verbose_name="مشغولة")

  def __str__(self):
    return self.name