
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

class Building(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('اسم المبني'))
    address = models.TextField(verbose_name=_('عنوان المبني'))
    description = models.TextField(blank=True, null=True, verbose_name=_('وصف'))
    image = models.ImageField(upload_to='building_images/', blank=True, null=True, verbose_name=_('صورة المبني'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    def total_units(self):
        return self.unit_set.count()

    def total_rent(self):
        return sum(unit.monlthly_rent for unit in self.unit_set.filter(status='rented'))

    def yearly_rent(self):
        return self.total_rent() * 12

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('مبنى')
        verbose_name_plural = _('المباني')
        ordering = ['name']

class Unit(models.Model):
    UNIT_TYPE_CHOICES = (
        ('Office', _('مكتب')),
        ('Apartment', _('شقة')),
        ('Shop', _('محل')),
    )
    UNIT_STATUS_CHOICES = (
        ('Available', _('متاحة')),
        ('Rented', _('مؤجرة')),
        ('Maintenance', _('تحت الصيانة')),
    )
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name=_('المبنى'))
    unit_type = models.CharField(max_length=50, choices=UNIT_TYPE_CHOICES, verbose_name=_('نوع الوحدة'))
    status = models.CharField(max_length=50, choices=UNIT_STATUS_CHOICES, verbose_name=_('الحالة'), default='Available')
    number = models.CharField(max_length=50, verbose_name=_('رقم الوحدة'))
    area = models.FloatField(verbose_name=_('المساحة'))
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name= _('الإجمالي الشهري'))
    image = models.ImageField(upload_to='unit_images/', blank=True, null=True, verbose_name=_('صورة الوحدة'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    def is_available(self):
        return self.status == 'Available'

    def yearly_rent(self):
        return self.monthly_rent * 12

    def __str__(self):
        return f'{self.get_unit_type_display()} - {self.number}'

    class Meta:
        verbose_name = _('وحدة')
        verbose_name_plural = _('الوحدات')
        indexes = [
            models.Index(fields=['status', 'unit_type']),
        ]

class Tenant(models.Model):
    full_name = models.CharField(max_length=200, verbose_name=_('الاسم الكامل'))
    phone_number = models.CharField(max_length=20, verbose_name=_('رقم الهاتف'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('البريد الإلكتروني'))
    description = models.TextField(blank=True, null=True, verbose_name=_('ملاحظات'))

    def active_contracts(self):
        return LeaseContract.objects.filter(tenant=self, is_active=True).count()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('مستأجر')
        verbose_name_plural = _('المستأجرون')

class LeaseContract(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name=_('الوحدة'))
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name=_('المستأجر'))
    start_date = models.DateField(verbose_name=_('تاريخ البدء'))
    end_date = models.DateField(verbose_name=_('تاريخ الانتهاء'))
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('الإيجار الشهري'))
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))

    def remaining_days(self):
        if self.end_date:
            delta = self.end_date - now().date()
            return delta.days
        return None

    def is_due_soon(self):
        remaining = self.remaining_days()
        return remaining is not None and remaining <= 30

    def __str__(self):
        return f'عقد إيجار: {self.unit} - {self.tenant}'

    class Meta:
        verbose_name = _('عقد إيجار')
        verbose_name_plural = _('عقود الايجار')
        ordering = ['-start_date']

class AuditLog(models.Model):
    action = models.CharField(max_length=200, verbose_name=_('الإجراء'))
    model_name = models.CharField(max_length=200, verbose_name=_('اسم النموذج'))
    object_id = models.PositiveIntegerField(verbose_name=_('معرف العنصر'))
    user = models.CharField(max_length=200, verbose_name=_('المستخدم'))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإجراء'))
    details = models.TextField(blank=True, null=True, verbose_name=_('تفاصيل'))

    def __str__(self):
        return f'{self.action} - {self.model_name} - {self.timestamp}'

    class Meta:
        verbose_name = _('سجل')
        verbose_name_plural = _('السجلات')
        ordering = ['-timestamp']

class Payment(models.Model):
    contract = models.ForeignKey(LeaseContract, on_delete=models.CASCADE, verbose_name=_('العقد'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('المبلغ'))
    payment_date = models.DateField(verbose_name=_('تاريخ الدفع'))
    description = models.TextField(blank=True, null=True, verbose_name=_('الوصف'))

    def __str__(self):
        return f'دفعة: {self.contract} - {self.amount}'

    class Meta:
        verbose_name = _('دفعة')
        verbose_name_plural = _('الدفعات')

class MaintenanceRequest(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name=_('الوحدة'))
    description = models.TextField(verbose_name=_('تفاصيل المشكلة'))
    request_date = models.DateField(verbose_name=_('تاريخ الطلب'))
    is_resolved = models.BooleanField(default=False, verbose_name=_('تمت معالجتها'))
    resolved_date = models.DateField(blank=True, null=True, verbose_name=_('تاريخ المعالجة'))

    def __str__(self):
        return f'طلب صيانة - {self.unit.number}'

    class Meta:
        verbose_name = _('طلب صيانة')
        verbose_name_plural = _('طلبات الصيانة')

class Expense(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name=_('المبنى'))
    description = models.TextField(verbose_name= _('وصف المصروف'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('المبلغ'))
    date = models.DateField(verbose_name=_('تاريخ المصروف'))

    def __str__(self):
        return f'{self.description} - {self.amount}'

    class Meta:
        verbose_name = _('مصروف')
        verbose_name_plural = _('المصاريف')

class Notifiction(models.Model):
    message = models.TextField(verbose_name=_('الرسالة'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    is_read = models.BooleanField(default=False, verbose_name=_('مقروء'))

    def __str__(self):
        return f'إشعار: {self.message[:20]}...'

    class Meta:
        verbose_name = _('إشعار')
        verbose_name_plural = _('الإشعارات')

class TenantBankAccount(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name=_('المستأجر'))
    bank_name = models.CharField(max_length=100, verbose_name=_('اسم البنك'))
    account_number = models.CharField(max_length=50, verbose_name=_('رقم الحساب'))
    iban = models.CharField(max_length=34, verbose_name=_('رقم البنك الإيباني'))

    def __str__(self):
        return f'{self.tenant.full_name}'

    class Meta:
        verbose_name = _('حساب مصرفي للمستأجر')
        verbose_name_plural = _('حسابات مصرفية للمستأجرين')

class RentReport(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name=_('المبنى'))
    total_income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('إجمالي الدخل'))
    generated_date = models.DateField(verbose_name=_('تاريخ التقرير'), auto_now_add=True)
    
    def __str__(self):
        return f'{self.building.number}'

    class Meta:
        verbose_name = _('تقرير الإيجار')
        verbose_name_plural = _('تقارير الإيجار')