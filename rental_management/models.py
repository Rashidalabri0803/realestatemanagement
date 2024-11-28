
from datetime import timedelta

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Building(models.Model):
    name = models.CharField(
        max_length=200, 
        verbose_name=_('اسم المبني')
    )
    address = models.TextField(verbose_name=_('عنوان المبني'))
    description = models.TextField(blank=True, null=True, verbose_name=_('وصف'))
    image = models.ImageField(
        upload_to='building_images/', 
        blank=True, 
        null=True, 
        verbose_name=_('صورة المبني')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('تاريخ التحديث'))

    def total_units(self):
        return self.units.count()

    def total_rent(self):
        return sum(unit.monlthly_rent for unit in self.units.filter(status='rented'))

    def yearly_rent(self):
        return self.total_rent() * 12

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('مبنى')
        verbose_name_plural = _('المباني')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

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
    
    building = models.ForeignKey(
        Building, 
        on_delete=models.CASCADE,
        related_name='units',
        verbose_name=_('المبنى')
    )
    unit_type = models.CharField(
        max_length=50, 
        choices=UNIT_TYPE_CHOICES, 
        verbose_name=_('نوع الوحدة')
    )
    status = models.CharField(
        max_length=50, 
        choices=UNIT_STATUS_CHOICES,
        default='Available',
        verbose_name=_('الحالة')
    )
    number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('رقم الوحدة')
    )
    area = models.FloatField(
        verbose_name=_('المساحة')
    )
    monthly_rent = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name= _('الإيجار الشهري')
    )
    image = models.ImageField(
        upload_to='unit_images/', 
        blank=True, 
        null=True, 
        verbose_name=_('صورة الوحدة')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('تاريخ الإنشاء')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('تاريخ التحديث')
    )

    def is_available(self):
        return self.status == 'Available'

    def yearly_rent(self):
        return self.monthly_rent * 12

    def __str__(self):
        return f'{self.get_unit_type_display()} - {self.number}'

    class Meta:
        verbose_name = _('وحدة')
        verbose_name_plural = _('الوحدات')
        ordering = ['building', 'number']
        indexes = [
            models.Index(fields=['status', 'unit_type']),
        ]

class MaintenanceRequest(models.Model):
    unit = models.ForeignKey(
        Unit, 
        on_delete=models.CASCADE,
        related_name= 'maintenance_requests',
        verbose_name=_('الوحدة')
    )
    description = models.TextField(
        verbose_name=_('وصف المشكلة')
    )
    request_date = models.DateField(
        default=now,
        verbose_name=_('تاريخ الطلب')
    )
    is_resolved = models.BooleanField(
        default=False, 
        verbose_name=_('تمت المعالجة')
    )
    resolved_date = models.DateField(
        blank=True, 
        null=True, 
        verbose_name=_('تاريخ المعالجة')
    )

    def __str__(self):
        return f'طلب صيانة للوحدة {self.unit.number} - {self.request_date}'

    class Meta:
        verbose_name = _('طلب صيانة')
        verbose_name_plural = _('طلبات الصيانة')
        ordering = ['-request_date']
        indexes = [
            models.Index(fields=['is_resolved']),
        ]

class Expense(models.Model):
    building = models.ForeignKey(
        Building, 
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name=_('المبنى')
    )
    description = models.TextField(
        verbose_name=_('الوصف')
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_('المبلغ')
    )
    date = models.DateField(
        default=now,
        verbose_name=_('التاريخ')
    )

    def __str__(self):
        return f'مصروف {self.description} - {self.amount} ({self.date})'

    class Meta:
        verbose_name = _('مصروف')
        verbose_name_plural = _('المصاريف')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['building', 'date']),
        ]

class AuditLog(models.Model):
    action = models.CharField(
        max_length=200, 
        verbose_name=_('الإجراء')
    )
    model_name = models.CharField(
        max_length=200, 
        verbose_name=_('اسم النموذج')
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('معرف العنصر')
    )
    user = models.CharField(
        max_length=200, 
        verbose_name=_('المستخدم')
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('تاريخ الإجراء')
    )
    details = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_('تفاصيل')
    )
    related_model = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_('النموذج المرتبط'),
        help_text=_('اسم النموذج المرتبط بالسجل')
    )

    def __str__(self):
        return f'{self.action} - {self.model_name} - {self.timestamp}'

    class Meta:
        verbose_name = _('سجل')
        verbose_name_plural = _('السجلات')
        ordering = ['-timestamp']
class Tenant(models.Model):
    full_name = models.CharField(
        max_length=200, 
        verbose_name=_('الاسم الكامل')
    )
    email = models.EmailField(
        verbose_name=_('البريد الإلكتروني')
    )
    phone_number = models.CharField(
        max_length=50, 
        verbose_name=_('رقم الهاتف')
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name=_('مفعل')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('تاريخ الإنشاء')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('تاريخ التحديث')
    )
    active_contracts = models.ManyToManyField(
        'LeaseContract', 
        related_name='active_tenants',
        verbose_name=_('العقود النشطة')
    )
    profile_picture_preview = models.ImageField(
        upload_to='tenant_profile_pictures/', 
        blank=True, 
        null=True, 
        verbose_name=_('صورة الملف الشخصي')
    )
    
class LeaseContract(models.Model):
    unit = models.ForeignKey(
        Unit, 
        on_delete=models.CASCADE,
        verbose_name=_('الوحدة')
    )
    tenant = models.ForeignKey(
        'Tenant', 
        on_delete=models.CASCADE,
        verbose_name=_('المستأجر')
    )
    start_date = models.DateField(
        default=now,
        verbose_name=_('تاريخ البدء')
    )
    end_date = models.DateField(
        verbose_name=_('تاريخ النهاية')
    )
    monthly_rent = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_('الإيجار الشهري')
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name=_('نشط')
    )

    def remainig_days(self):
        if self.end_date:
            delta = self.end_date - now().date()
            return delta.days
        return None

    def is_due_soon(self):
        remaining = self.remainig_days()
        return remaining is not None and remaining <= 30

    def generate_invoice(self):
        invoice = Invoice.objects.create(
            contract=self,
            issue_date=now().date(),
            due_date=now().date() + timedelta(days=30),
            amount=self.monthly_rent,
        )
        return invoice

    def __str__(self):
        return f'عقد إيجار: {selef.unit} - {self.tenant}'

    class Meta:
        verbose_name = _('عقد إيجار')
        verbose_name_plural = _('عقود الإيجار')
        ordering = ['-start_date']
class Invoice(models.Model):
    contract = models.ForeignKey(
        'LeaseContract', 
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name=_('العقد')
    )
    issue_date = models.DateField(
        default=now,
        verbose_name=_('تاريخ الإصدار')
    )
    due_date = models.DateField(
        verbose_name=_('تاريخ الاستحقاق')
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_('المبلغ')
    )
    is_paid = models.BooleanField(
        default=False, 
        verbose_name=_('مدفوعة')
    )

    def days_until_due(self):
        if self.due_date:
            delta = self.due_date - now().date()
            return delta.days
        return None

    def __str__(self):
        return f'فاتورة {self.id} - {self.contract.unit.number} - {self.amount}'

    class Meta:
        verbose_name = _('فاتورة')
        verbose_name_plural = _('الفواتير')
        ordering = ['-issue_date']
        indexes = [
            models.Index(fields=['contract', 'due_date']),
        ]

class Reminder(models.Model):
    tenant = models.ForeignKey(
        'Tenant', 
        on_delete=models.CASCADE,
        related_name='reminders',
        verbose_name=_('الأشخاص')
    )
    contract = models.ForeignKey(
        'LeaseContract', 
        on_delete=models.CASCADE,
        related_name='reminders',
        verbose_name=_('العقد')
    )
    message = models.TextField(
        verbose_name=_('الرسالة التذكير')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('تاريخ الإنشاء')
    )
    is_sent = models.BooleanField(
        default=False, 
        verbose_name=_('تم إرساله')
    )

    def __str__(self):
        return f'تذكير {self.tenant.full_name}'

    class Meta:
        verbose_name = _('تذكير')
        verbose_name_plural = _('التذكيرات')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'is_sent']),
        ]

class Notification(models.Model):
    message = models.TextField(
        verbose_name=_('الرسالة')
    )
    is_read = models.BooleanField(
        default=False, 
        verbose_name=_('مقروء')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('تاريخ الإنشاء')
    )
    related_model = models.CharField(
        max_length=100, 
        blank=True,
        null=True,
        verbose_name=_('النموذج المرتبط'),
        help_text=_('اسم النموذج المرتبط (مثل: LeaseContract أو Invoce)')
    )
    related_id = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        verbose_name=_('المعرف المرتبط'),
        help_text=_('معرف العنصر المرتبط في النموذج')
    )

    def __str__(self):
        return f'إشعار: {self.message[:20]}'

    class Meta:
        verbose_name = _('إشعار')
        verbose_name_plural = _('الإشعارات')
        ordering = ['-created_at']

class Subscription(models.Model):
    tenant = models.ForeignKey(
        'Tenant', 
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name=_('المستأجر')
    )
    name = models.CharField(
        max_length=200, 
        verbose_name=_('اسم الاشتراك')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('وصف')
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_('سعر الاشتراك الشهري')
    )
    start_date = models.DateField(
        default=now,
        verbose_name=_('تاريخ البدء')
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('تاريخ النهاية')
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name=_('نشط')
    )

    def remaining_days(self):
        if self.end_date:
            delta = self.end_date - now().date()
            return delta.days
        return None

    def __str__(self):
        return f'اشتراك: {self.name} - {self.tenant.full_name}'

    class Meta:
        verbose_name = _('اشتراك')
        verbose_name_plural = _('الاشتراكات')
        ordering = ['-start_date']

class Report(models.Model):
    name = models.CharField(
        max_length=200, 
        verbose_name=_('اسم التقرير')
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_('وصف')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('تاريخ الإنشاء')
    )
    last_generated = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name=_('آخر توليد')
    )

    def generate_report(self):
        self.last_generated = now()
        self.save()

    def __str__(self):
        return f'تقرير: {self.name}'

    class Meta:
        verbose_name = _('تقرير')
        verbose_name_plural = _('التقارير')
        ordering = ['-created_at']

class Payment(models.Model):
    pass