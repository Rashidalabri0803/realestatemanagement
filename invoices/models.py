from django.db import models

from contracts.models import Contract


class Invoice(models.Model):
  contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name="العقد")
  issue_date = models.DateField(verbose_name="تاريخ الاصدار")
  due_date = models.DateField(verbose_name="تاريخ الاستحقاق")
  amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ")
  status = models.CharField(max_length=20, choices=[('paid', 'مدفوعة'),('unpaid', 'غير مدفوعة')], default='unpaid', verbose_name="الحالة")

  def __str__(self):
    return f"فاتورة: {self.contract} - {self.amount}"