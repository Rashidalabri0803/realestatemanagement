        from django.db import models
        from django.utils.translation import gettext_lazy as _
        from django.utils.timezone import now
        from datetime import timedelta
        from django.contrib.auth.models import User


        ### نموذج أساسي لدعم الحذف المنطقي ###
        class BaseModel(models.Model):
            is_deleted = models.BooleanField(default=False, verbose_name=_("محذوف"))
            created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإنشاء"))
            updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاريخ التحديث"))

            class Meta:
                abstract = True


        ### نموذج المباني ###
        class Building(BaseModel):
            name = models.CharField(max_length=200, unique=True, verbose_name=_("اسم المبنى"))
            address = models.TextField(verbose_name=_("عنوان المبنى"))
            description = models.TextField(blank=True, null=True, verbose_name=_("وصف"))
            image = models.ImageField(upload_to='building_images/', blank=True, null=True, verbose_name=_("صورة المبنى"))

            def total_units(self):
                return self.units.filter(is_deleted=False).count()

            def rented_units(self):
                return self.units.filter(status='rented', is_deleted=False).count()

            def rented_percentage(self):
                total = self.total_units()
                return (self.rented_units() / total) * 100 if total > 0 else 0

            def total_rent(self):
                return sum(unit.monthly_rent for unit in self.units.filter(status='rented', is_deleted=False))

            def yearly_rent(self):
                return self.total_rent() * 12

            def monthly_income(self):
                return self.total_rent() - sum(expense.amount for expense in self.expenses.filter(is_deleted=False))

            def yearly_income(self):
                return self.monthly_income() * 12

            def __str__(self):
                return self.name

            class Meta:
                verbose_name = _("مبنى")
                verbose_name_plural = _("المباني")
                ordering = ['name']
                indexes = [models.Index(fields=['name'])]


        ### نموذج الوحدات ###
        class Unit(BaseModel):
            UNIT_TYPE_CHOICES = [
                ('office', _("مكتب")),
                ('apartment', _("شقة")),
                ('shop', _("محل")),
                ('warehouse', _("مستودع")),
            ]
            UNIT_STATUS_CHOICES = [
                ('available', _("متاحة")),
                ('rented', _("مؤجرة")),
                ('maintenance', _("تحت الصيانة")),
                ('reserved', _("محجوزة")),
            ]

            building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="units", verbose_name=_("المبنى"))
            unit_type = models.CharField(max_length=50, choices=UNIT_TYPE_CHOICES, verbose_name=_("نوع الوحدة"))
            status = models.CharField(max_length=50, choices=UNIT_STATUS_CHOICES, default='available', verbose_name=_("الحالة"))
            tags = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("تصنيفات"))
            number = models.CharField(max_length=50, unique=True, verbose_name=_("رقم الوحدة"))
            area = models.FloatField(verbose_name=_("المساحة (م²)"))
            monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("الإيجار الشهري"))
            image = models.ImageField(upload_to='unit_images/', blank=True, null=True, verbose_name=_("صورة الوحدة"))

            def yearly_rent(self):
                return self.monthly_rent * 12

            def is_available(self):
                return self.status == 'available'

            def __str__(self):
                return f"{self.get_unit_type_display()} - {self.number}"

            class Meta:
                verbose_name = _("وحدة")
                verbose_name_plural = _("الوحدات")
                ordering = ['building', 'number']
                indexes = [models.Index(fields=['status', 'unit_type', 'tags'])]


        ### نموذج المستأجرين ###
        class Tenant(BaseModel):
            full_name = models.CharField(max_length=200, verbose_name=_("الاسم الكامل"))
            phone_number = models.CharField(max_length=20, unique=True, verbose_name=_("رقم الهاتف"))
            email = models.EmailField(blank=True, null=True, verbose_name=_("البريد الإلكتروني"))
            id_card = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("رقم الهوية"))
            profile_picture = models.ImageField(upload_to='tenant_pictures/', blank=True, null=True, verbose_name=_("صورة المستأجر"))
            description = models.TextField(blank=True, null=True, verbose_name=_("ملاحظات"))

            def active_contracts(self):
                return self.leasecontract_set.filter(is_active=True, is_deleted=False).count()

            def __str__(self):
                return self.full_name

            class Meta:
                verbose_name = _("مستأجر")
                verbose_name_plural = _("المستأجرون")
                ordering = ['full_name']
                indexes = [models.Index(fields=['phone_number'])]
class LeaseContract(BaseModel):
    unit = models.OneToOneField(Unit, on_delete=models.CASCADE, related_name="contract", verbose_name=_("الوحدة"))
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="contracts", verbose_name=_("المستأجر"))
    start_date = models.DateField(verbose_name=_("تاريخ البدء"))
    end_date = models.DateField(verbose_name=_("تاريخ الانتهاء"))
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("الإيجار الشهري"))
    is_active = models.BooleanField(default=True, verbose_name=_("نشط"))

    def remaining_days(self):
        if self.end_date:
            delta = self.end_date - now().date()
            return delta.days
        return None

    def generate_invoice(self):
        return Invoice.objects.create(
            contract=self,
            issue_date=now().date(),
            due_date=now().date() + timedelta(days=30),
            amount=self.monthly_rent
        )

    def __str__(self):
        return f"عقد إيجار: {self.unit} - {self.tenant}"

    class Meta:
        verbose_name = _("عقد إيجار")
        verbose_name_plural = _("عقود الإيجار")
        ordering = ['-start_date']
class Invoice(BaseModel):
    contract = models.ForeignKey(LeaseContract, on_delete=models.CASCADE, related_name="invoices", verbose_name=_("العقد"))
    issue_date = models.DateField(default=now, verbose_name=_("تاريخ الإصدار"))
    due_date = models.DateField(verbose_name=_("تاريخ الاستحقاق"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("المبلغ"))
    is_paid = models.BooleanField(default=False, verbose_name=_("مدفوعة"))
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("غرامة التأخير"))

    def calculate_late_fee(self):
        if not self.is_paid and self.due_date < now().date():
            days_late = (now().date() - self.due_date).days
            self.late_fee = days_late * 5  # غرامة يومية 5 وحدات
            return self.late_fee
        return 0

    def is_overdue(self):
        return not self.is_paid and self.due_date < now().date()

    def __str__(self):
        return f"فاتورة {self.id} - {self.amount} ({'مدفوعة' if self.is_paid else 'غير مدفوعة'})"

    class Meta:
        verbose_name = _("فاتورة")
        verbose_name_plural = _("الفواتير")
        ordering = ['-issue_date']
        indexes = [
            models.Index(fields=['tenant', 'is_paid']),
            models.Index(fields=['due_date']),
        ]

class Currency(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("اسم العملة"))
    symbol = models.CharField(max_length=10, verbose_name=_("رمز العملة"))
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=_("سعر الصرف بالنسبة للعملة الأساسية"))

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    class Meta:
        verbose_name = _("عملة")
        verbose_name_plural = _("العملات")
        ordering = ['name']
        
class Payment(BaseModel):
    contract = models.ForeignKey(LeaseContract, on_delete=models.CASCADE, related_name="payments", verbose_name=_("العقد"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("المبلغ"))
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, verbose_name=_("العملة"))
    payment_date = models.DateField(default=now, verbose_name=_("تاريخ الدفع"))
    description = models.TextField(blank=True, null=True, verbose_name=_("وصف"))

    def __str__(self):
        return f"مدفوعات: {self.contract.unit.number} - {self.amount} ({self.payment_date})"

    class Meta:
        verbose_name = _("مدفوعات")
        verbose_name_plural = _("المدفوعات")
        ordering = ['-payment_date']
        indexes = [models.Index(fields=['contract', 'payment_date'])]
        
class Reminder(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="reminders", verbose_name=_("المستأجر"))
    contract = models.ForeignKey(LeaseContract, on_delete=models.CASCADE, related_name="reminders", blank=True, null=True, verbose_name=_("العقد"))
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="reminders", blank=True, null=True, verbose_name=_("الفاتورة"))
    message = models.TextField(verbose_name=_("رسالة التذكير"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإنشاء"))
    is_sent = models.BooleanField(default=False, verbose_name=_("تم الإرسال"))

    def send_reminder(self):
        if not self.is_sent:
            # محاكاة إرسال الإشعار
            print(f"تم إرسال التذكير إلى {self.tenant.full_name}")
            self.is_sent = True
            self.save()

    def __str__(self):
        return f"تذكير: {self.tenant.full_name} - {self.message[:20]}"

    class Meta:
        verbose_name = _("تذكير")
        verbose_name_plural = _("التذكيرات")
        ordering = ['-created_at']
class Notification(BaseModel):
    message = models.TextField(verbose_name=_("الرسالة"))
    is_read = models.BooleanField(default=False, verbose_name=_("مقروء"))
    priority = models.CharField(
        max_length=50, 
        choices=[('low', _("منخفضة")), ('medium', _("متوسطة")), ('high', _("عالية"))], 
        default='low', 
        verbose_name=_("الأولوية")
    )
    related_model = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("النموذج المرتبط"))
    related_id = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("المعرّف المرتبط"))

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"إشعار: {self.message[:20]}{'...' if len(self.message) > 20 else ''}"

    class Meta:
        verbose_name = _("إشعار")
        verbose_name_plural = _("الإشعارات")
        ordering = ['-created_at']
class Subscription(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="subscriptions", verbose_name=_("المستأجر"))
    service_name = models.CharField(max_length=200, verbose_name=_("اسم الخدمة"))
    service_type = models.CharField(
        max_length=100, 
        choices=[('internet', _("إنترنت")), ('parking', _("مواقف سيارات")), ('utilities', _("فواتير خدمات")), ('other', _("أخرى"))], 
        default='other', 
        verbose_name=_("نوع الخدمة")
    )
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("التكلفة الشهرية"))
    start_date = models.DateField(default=now, verbose_name=_("تاريخ البدء"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("تاريخ الانتهاء"))
    is_active = models.BooleanField(default=True, verbose_name=_("نشط"))

    def __str__(self):
        return f"اشتراك: {self.service_name} - {self.tenant.full_name}"

    class Meta:
        verbose_name = _("اشتراك")
        verbose_name_plural = _("الاشتراكات")
        ordering = ['-start_date']
class AuditLog(BaseModel):
    action = models.CharField(max_length=200, verbose_name=_("الإجراء"))
    model_name = models.CharField(max_length=200, verbose_name=_("اسم النموذج"))
    object_id = models.PositiveIntegerField(verbose_name=_("معرّف العنصر"))
    user = models.CharField(max_length=200, verbose_name=_("المستخدم"))
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_("عنوان IP"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإجراء"))
    details = models.TextField(blank=True, null=True, verbose_name=_("تفاصيل"))

    def __str__(self):
        return f"{self.action} - {self.model_name} - {self.timestamp}"

    class Meta:
        verbose_name = _("سجل")
        verbose_name_plural = _("السجلات")
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['model_name', 'timestamp'])]
class SystemSettings(BaseModel):
    key = models.CharField(max_length=200, unique=True, verbose_name=_("اسم الإعداد"))
    value = models.TextField(verbose_name=_("القيمة"))
    description = models.TextField(blank=True, null=True, verbose_name=_("الوصف"))

    def __str__(self):
        return f"إعداد: {self.key}"

    class Meta:
        verbose_name = _("إعداد النظام")
        verbose_name_plural = _("إعدادات النظام")
        ordering = ['key']
class SystemStatistics(BaseModel):
    date = models.DateField(default=now, verbose_name=_("التاريخ"))
    total_buildings = models.PositiveIntegerField(default=0, verbose_name=_("إجمالي المباني"))
    total_units = models.PositiveIntegerField(default=0, verbose_name=_("إجمالي الوحدات"))
    total_tenants = models.PositiveIntegerField(default=0, verbose_name=_("إجمالي المستأجرين"))
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("إجمالي الإيرادات"))

    def __str__(self):
        return f"إحصائية النظام - {self.date}"

    class Meta:
        verbose_name = _("إحصائية النظام")
        verbose_name_plural = _("إحصائيات النظام")
        ordering = ['-date']
        indexes = [models.Index(fields=['date'])]
class LatePayment(BaseModel):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name="late_payment", verbose_name=_("الفاتورة"))
    days_late = models.PositiveIntegerField(verbose_name=_("عدد الأيام المتأخرة"))
    penalty = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("غرامة التأخير"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ التسجيل"))

    def calculate_penalty(self, daily_rate=5):
        """حساب الغرامة اليومية"""
        self.penalty = self.days_late * daily_rate
        self.save()

    def __str__(self):
        return f"غرامة: {self.penalty} - {self.days_late} يوم ({self.invoice})"

    class Meta:
        verbose_name = _("مدفوعات متأخرة")
        verbose_name_plural = _("مدفوعات متأخرة")
        ordering = ['-created_at']

class Language(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("اللغة"))
    code = models.CharField(max_length=10, unique=True, verbose_name=_("رمز اللغة"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("لغة")
        verbose_name_plural = _("اللغات")
        ordering = ['name']
        
class Report(BaseModel):
    name = models.CharField(max_length=200, verbose_name=_("اسم التقرير"))
    report_type = models.CharField(max_length=100, verbose_name=_("نوع التقرير"))
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, verbose_name=_("اللغة"))
    filters = models.TextField(blank=True, null=True, verbose_name=_("الفلاتر"))
    content = models.TextField(verbose_name=_("محتوى التقرير"))
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإنشاء"))

    def generate_summary(self):
        """إنشاء ملخص للتقرير."""
        return f"تقرير: {self.name} - نوع: {self.report_type} - أنشئ في: {self.generated_at}"

    def __str__(self):
        return f"تقرير: {self.name} ({self.report_type})"

    class Meta:
        verbose_name = _("تقرير")
        verbose_name_plural = _("التقارير")
        ordering = ['-generated_at']
        
class SystemEvent(BaseModel):
    EVENT_TYPE_CHOICES = [
        ('info', _("معلومات")),
        ('warning', _("تحذير")),
        ('error', _("خطأ")),
    ]

    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, verbose_name=_("نوع الحدث"))
    description = models.TextField(verbose_name=_("الوصف"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("وقت الحدث"))

    def __str__(self):
        return f"حدث: {self.get_event_type_display()} - {self.timestamp}"

    class Meta:
        verbose_name = _("حدث النظام")
        verbose_name_plural = _("أحداث النظام")
        ordering = ['-timestamp']
class Feedback(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="feedbacks", verbose_name=_("المستأجر"))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="feedbacks", verbose_name=_("الوحدة"))
    comment = models.TextField(verbose_name=_("التعليق"))
    rating = models.PositiveIntegerField(default=5, verbose_name=_("التقييم"), help_text=_("من 1 إلى 5"))

    def __str__(self):
        return f"تعليق: {self.tenant.full_name} - {self.unit.number}"

    class Meta:
        verbose_name = _("تعليق")
        verbose_name_plural = _("تعليقات")
        ordering = ['-created_at']
class ReminderLog(BaseModel):
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE, related_name="logs", verbose_name=_("التذكير"))
    sent_date = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإرسال"))
    status = models.CharField(
        max_length=50, 
        choices=[('success', _("ناجح")), ('failed', _("فشل"))], 
        default='success', 
        verbose_name=_("الحالة")
    )
    response_details = models.TextField(blank=True, null=True, verbose_name=_("تفاصيل الرد"))

    def __str__(self):
        return f"سجل تذكير: {self.reminder.id} - {self.get_status_display()}"

    class Meta:
        verbose_name = _("سجل التذكير")
        verbose_name_plural = _("سجلات التذكيرات")
        ordering = ['-sent_date']
class DailyPaymentLog(BaseModel):
    date = models.DateField(default=now, verbose_name=_("التاريخ"))
    total_payments = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("إجمالي المدفوعات"))
    total_invoices = models.PositiveIntegerField(default=0, verbose_name=_("عدد الفواتير"))
    total_late_payments = models.PositiveIntegerField(default=0, verbose_name=_("عدد الفواتير المتأخرة"))

    def __str__(self):
        return f"سجل الدفع اليومي - {self.date}"

    class Meta:
        verbose_name = _("سجل الدفع اليومي")
        verbose_name_plural = _("سجلات الدفع اليومية")
        ordering = ['-date']
        indexes = [models.Index(fields=['date'])]
class ScheduledReminder(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="scheduled_reminders", verbose_name=_("المستأجر"))
    contract = models.ForeignKey(LeaseContract, on_delete=models.CASCADE, related_name="scheduled_reminders", verbose_name=_("العقد"))
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True, related_name="scheduled_reminders", verbose_name=_("الفاتورة"))
    scheduled_date = models.DateTimeField(verbose_name=_("تاريخ التذكير المجدول"))
    is_sent = models.BooleanField(default=False, verbose_name=_("تم الإرسال"))

    def send_reminder(self):
        if not self.is_sent and self.scheduled_date <= now():
            # محاكاة الإرسال
            print(f"تم إرسال التذكير إلى {self.tenant.full_name}")
            self.is_sent = True
            self.save()

    def __str__(self):
        return f"تذكير مجدول: {self.tenant.full_name} - {self.scheduled_date}"

    class Meta:
        verbose_name = _("تذكير مجدول")
        verbose_name_plural = _("تذكيرات مجدولة")
        ordering = ['-scheduled_date']
        indexes = [models.Index(fields=['tenant', 'scheduled_date', 'is_sent'])]
class UserRole(BaseModel):
    ROLE_CHOICES = [
        ('admin', _("مدير")),
        ('manager', _("مدير عمليات")),
        ('staff', _("موظف")),
    ]

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True, verbose_name=_("الدور"))
    description = models.TextField(blank=True, null=True, verbose_name=_("الوصف"))

    def __str__(self):
        return f"دور: {self.get_name_display()}"

    class Meta:
        verbose_name = _("دور المستخدم")
        verbose_name_plural = _("أدوار المستخدمين")
        ordering = ['name']
class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name=_("المستخدم"))
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, related_name="users", verbose_name=_("الدور"))
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("رقم الهاتف"))
    address = models.TextField(blank=True, null=True, verbose_name=_("العنوان"))

    def __str__(self):
        return f"ملف المستخدم: {self.user.username}"

    class Meta:
        verbose_name = _("ملف المستخدم")
        verbose_name_plural = _("ملفات المستخدمين")
class MessageLog(BaseModel):
    recipient = models.CharField(max_length=200, verbose_name=_("المستلم"))
    message = models.TextField(verbose_name=_("الرسالة"))
    sent_date = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإرسال"))
    status = models.CharField(
        max_length=50, 
        choices=[('sent', _("تم الإرسال")), ('failed', _("فشل"))], 
        default='sent', 
        verbose_name=_("الحالة")
    )
    response_details = models.TextField(blank=True, null=True, verbose_name=_("تفاصيل الرد"))

    def __str__(self):
        return f"سجل الرسائل: {self.recipient} - {self.get_status_display()}"

    class Meta:
        verbose_name = _("سجل الرسائل")
        verbose_name_plural = _("سجلات الرسائل")
        ordering = ['-sent_date']

class DailyActivityLog(BaseModel):
    date = models.DateField(default=now, verbose_name=_("التاريخ"))
    total_logins = models.PositiveIntegerField(default=0, verbose_name=_("إجمالي تسجيلات الدخول"))
    total_payments = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("إجمالي المدفوعات"))
    total_invoices = models.PositiveIntegerField(default=0, verbose_name=_("إجمالي الفواتير"))
    total_reminders_sent = models.PositiveIntegerField(default=0, verbose_name=_("التذكيرات المرسلة"))

    def __str__(self):
        return f"سجل الأنشطة اليومية - {self.date}"

    class Meta:
        verbose_name = _("سجل الأنشطة اليومية")
        verbose_name_plural = _("سجلات الأنشطة اليومية")
        ordering = ['-date']
        indexes = [models.Index(fields=['date'])]