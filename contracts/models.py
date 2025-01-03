from django.db import models
from tenants.models import Tenant
from properties.models import Property

class LeasContract(models.Model):
  tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name="المستأجر")
  property = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name="العقار")
  start_date = models.DateField(verbose_name="تاريخ البدء")
  end_date = models.DateField(verbose_name="تاريخ النهاية")
  monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الإيجار الشهري")
  is_active = models.BooleanField(default=True, verbose_name="نشط")

  def __str__(self):
    return f"{self.tenant.name} - {self.property.name}"

  class Meta:
    verbose_name = "عقد إيجار"
    verbose_name_plural = "عقود الإيجار"