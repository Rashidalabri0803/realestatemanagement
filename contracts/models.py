from django.db import models

from properties.models import Property


class Contract(models.Model):
  property = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name="الوحدة")
  tenant_name = models.CharField(max_length=255, verbose_name="اسم المستأجر")
  start_date = models.DateField(verbose_name="تاريخ البداية")
  end_date = models.DateField(verbose_name="تاريخ النهاية")
  terms = models.TextField(verbose_name="الشروط العقد", blank=True, null=True)

  def __str__(self):
    return f"عقد: {self.property.name} - {self.tenant_name}"