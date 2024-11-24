from django.db import models
from django.utils.translation import gettext_lazy as _


# نموذج المبني
class Building(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('اسم المبني'))
    address = models.CharField(max_length=200, verbose_name=_('عنوان المبني'))
    description = models.TextField(blank=True, null=True, verbose_name=_('وصف'))
    image = models.ImageField(upload_to='building_images/', blank=True, null=True, verbose_name=_('صورة المبني'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    def __str__(self):
        return self.name

# نموذج الوحدة (مكتب، شقة، محل)
class Unit(models.Model):
  UNIT_TYPE_CHOICES = [
    ('office', _('مكتب')),
    ('apartment', _('شقة')),
    ('shope', _('متجر')),
  ]
  UNIT_TYPE_CHOICES = [
    ('avaliable', _('متاحة')),
    ('rented', _('مؤجرة')),
    ('maintenance', _('تحت الصيانة')),
  ]
  building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name=_('المبني'))
  unit_type = models.CharField(max_length=50, choices=UNIT_TYPE_CHOICES, verbose_name=_('نوع الوحدة'))
  status = models.CharField(max_length=50, choices=UNIT_TYPE_CHOICES, default='available', verbose_name=_('الحالة'))
  number = models.CharField(max_length=50, verbose_name=_('رقم الوحدة'))
  area = models.FloatField(verbose_name=_('المساحة (متر مربع)'))
  monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('الإيجار الشهري'))
image = models.ImageField(upload_to='unit_images/', blank=True, null=True, verbose_name=_('صورة الوحدة'))
created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))
    
def __str__(self):
    return f'{self.get_unit_type_display()} - {self.number}'

# نموذج المستأجر
class Tenant(models.Model):
    full_name = models.CharField(max_length=200, verbose_name=_('الاسم الكامل'))
    phone_number = models.CharField(max_length=200, verbose_name=_('رقم الهاتف'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('البريد الإلكتروني'))
    description = models.TextField(blank=True, null=True, verbose_name=_('ملاحظات'))

    def __str__(self):
        return self.full_name

# نموذج عقد الإيجار
class LeaseContract(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name=_('المستأجر'))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name=_('الوحدة'))
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