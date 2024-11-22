from django.db import models
from django.utils.translation import gettext_lazy as _

# نموذج المبني
class Building(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('اسم المبني'))
    address = models.CharField(max_length=200, verbose_name=_('عنوان المبني'))
    description = models.TextField(blank=True, null=True, verbose_name=_('وصف'))

    def __str__(self):
        return self.name

# نموذج الوحدة (مكتب، شقة، محل)
class Units(models.Model):
  UNIT_TYPE_CHOICES = [
    ('office', _('مكتب')),
    ('apartment', _('شقة')),
    ('shope', _('متجر')),
  ]
  building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name=_('المبني'))
  unit_type = models.CharField(max_length=50, choices=UNIT_TYPE_CHOICES, verbose_name=_('نوع الوحدة'))
  number = models.CharField(max_length=50, verbose_name=_('رقم الوحدة'))
  area = models.FloatField(verbose_name=_('المساحة (متر مربع)'))
  monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('الإيجار الشهري'))
  is_available = models.BooleanField(default=True, verbose_name=_('متاحة'))
    
  def __str__(self):
    return f'{self.unit_type} - {self.number}'

# نموذج المستأجر
class Tenant(models.Model):
    full_name = models.CharField(max_length=200, verbose_name=_('الاسم الكامل'))
    phone_number = models.CharField(max_length=200, verbose_name=_('رقم الهاتف'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('البريد الإلكتروني'))

    def __str__(self):
        return self.full_name

# نموذج عقد الإيجار
class LeaseContract(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name=_('المستأجر'))
    unit = models.ForeignKey(Units, on_delete=models.CASCADE, verbose_name=_('الوحدة'))
    start_date = models.DateField(verbose_name=_('تاريخ بدء العقد'))
    end_date = models.DateField(verbose_name=_('تاريخ انتهاء العقد'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('إجمالي قيمة العقد'))
    is_active = models.BooleanField(default=True, verbose_name=_('العقد نط'))
    document = models.FileField(upload_to='contracts/', blank=True, null=True, verbose_name=_('مستند العقد'))

    def __str__(self):
        return f'عقد إيجار: {self.tenant.full_name} - {self.unit}'

# نموذج الفواتير
class Invoice(models.Model):
    contract = models.ForeignKey(LeaseContract, on_delete=models.CASCADE, verbose_name=_('العقد'))
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('المبلغ المستحق'))
    due_date = models.DateField(verbose_name=_('تاريخ الاستحقاق'))
    is_paid = models.BooleanField(default=False, verbose_name=_('مدفوع'))
    payment_date = models.DateField(blank=True, null=True, verbose_name=_('تاريخ الدفع'))

    def __str__(self):
        return f'فاتورة لـــــ: {self.contract.tentant.full_name} - {self.amount_due}'