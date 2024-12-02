from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.contrib.auth.models import User
from datetime import timedelta

class AbstractBaseModel(models.Model):
    created_by = models.ForeignKey(
      User, 
      on_delete=models.SET_NULL, 
      null=True,
      blank=True,
      related_name="created_%(class)s",
      verbose_name=_("أنشي بواسطة"),
    )
    updated_by = models.ForeignKey(
      User, 
      on_delete=models.SET_NULL, 
      null=True,
      blank=True,
      related_name="updated_%(class)s",
      verbose_name=_("عدل بواسطة"),
    )
    is_deleted = models.BooleanField(
      default=False,
      verbose_name=_("محذوف"),
    )
    created_at = models.DateTimeField(
      auto_now_add=True,
      verbose_name=_("تاريخ إنشاء"),
    )
    updated_at = models.DateTimeField(
      auto_now=True,
      verbose_name=_("تاريخ التحديث"),
    )

    class Meta:
        abstract = True

class Building(AbstractBaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_("اسم المبنى"),
    )
    address = models.TextField(
        verbose_name=_("عنوان المبنى"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("وصف"),
    )
    image = models.ImageField(
        upload_to="building_images/",
        blank=True,
        null=True,
        verbose_name=_("صورة المبنى"),
    )

    def total_units(self):
        return self.units.filter(is_deleted=False).count()

    def rented_units(self):
        return self.units.filter(status='rented', is_deleted=False).count()

    def rented_percentage(self):
        total = self.total_units()
        return (self.rented_units() / total) * 100 if total > 0 else 0

    def monthly_income(self):
        return sum(invoice.amount for invoice in Invoice.objects.filter(contract__unit__building=self, is_paid=True))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("مبنى")
        verbose_name_plural = _("المباني")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

class Unit(AbstractBaseModel):
    UNIT_TYPE_CHOICES = (
        ('office', _('مكتب')),
        ('apartment', _('شقة')),
        ('store', _('محل')),
        ('warehouse', _('مستودع')),
    )
    UNIT_STATUS_CHOICES = (
        ('available', _('متاحة')),
        ('rented', _('مؤجرة')),
        ('maintenance', _('تحت الصيانة'))
        ('reserved', _('محجوزة')),
    )
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="units",
        verbose_name=_("المبنى"),
    )
    unit_type = models.CharField(
        max_length=50,
        choices=UNIT_TYPE_CHOICES,
        verbose_name=_("نوع الوحدة"),
    )
    status = models.CharField(
        max_length=50,
        unique=True,
        choices=UNIT_STATUS_CHOICES,
        default='available',
        verbose_name=_("الحالة"),
    )
    number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("رقم الوحدة"),
    )
    area = models.FloatField(
        verbose_name=_("مساحة (م2)")
    )
    monthly_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("الإيجار الشهري"),
    )

    def yearly_rent(self):
        return self.monthly_rent * 12

    def is_available(self):
        return self.status == 'available'

    def __str__(self):
        return f"{self.get_unit_type_display()} - {self.number}"

    class Meta:
        verbose_name = _("وحدة")
        verbose_name_plural = _("الوحدات")
        ordering = ["building", "number"]
        indexes = [
            models.Index(fields=["status", "unit_type", "building"]),
        ]

class Tenant(AbstractBaseModel):
    full_name = models.CharField(
        max_length=200,
        verbose_name=_("الاسم الكامل"),
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("رقم الهاتف"),
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_("البريد الإلكتروني"),
    )
    id_card = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("رقم الهوية"),
    )
    profile_picture = models.ImageField(
        upload_to="tenant_pictures/",
        blank=True,
        null=True,
        verbose_name=_("صورة المستأجر"),
    )

    def active_contracts_count(self):
        return self.contracts.filter(is_active=True, is_deleted=False).count()

    def total_payments(self):
        return sum(payment.amount for payment in self.payments.all())

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _("مستأجر")
        verbose_name_plural = _("المستأجرون")
        ordering = ["full_name"]
        indexes = [
            models.Index(fields=["phone_number", "email"]),
        ]

class LeaseContract(AbstractBaseModel):
    unit = models.OneToOneField(
        Unit,
        on_delete=models.CASCADE,
        related_name="contract",
        verbose_name=_("الوحدة"),
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="contracts",
        verbose_name=_("المستأجر"),
    )
    start_date = models.DateField(
        verbose_name=_("تاريخ البدء"),
    )
    end_date = models.DateField(
        verbose_name=_("تاريخ الانتهاء"),
    )
    monthly_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("الإيجار الشهري"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("نشط"),
    )

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
            amount=self.monthly_rent,
        )

    def __str__(self):
        return f"عقد إيجار: {self.unit} - {self.tenant}"

    class Meta:
        verbose_name = _("عقد إيجار")
        verbose_name_plural = _("عقود الإيجار")
        ordering = ["-start_date"]
        indexes = [
            models.Index(fields=["is_active", "tenant", "unit"]),
        ]

class Invoice(AbstractBaseModel):
    contract = models.ForeignKey(
        LeaseContract,
        on_delete=models.CASCADE,
        related_name="invoices",
        verbose_name=_("العقد"),
    )
    issue_date = models.DateField(
        default=now,
        verbose_name=_("تاريخ الإصدار"),
    )
    due_date = models.DateField(
        verbose_name=_("تاريخ الاستحقاق"),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("المبلغ"),
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name=_("مدفوعة"),
    )
    late_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("غرامة التأخير"),
    )

    def calculate_late_fee(self):
        if not self.is_paid and self.due_date < now().date():
            days_late = (now().date() - self.due_date).days
            self.late_fee = days_late * 5
            return self.late_fee
        return 0

    def is_overdue(self):
        return not self.is_paid and self.due_date < now().date()

    def __str__(self):
        return f"فاتورة: {self.id} - {self.amount} ({'مدفوعة' if self.is_paid else 'غير مدفوعة'})"

    class Meta:
        verbose_name = _("فاتورة")
        verbose_name_plural = _("الفواتير")
        ordering = ["-issue_date"]
        indexes = [
            models.Index(fields=["is_paid", "due_date"]),
        ]

class Payment(AbstractBaseModel):
    contract = models.ForeignKey(
        LeaseContract,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("العقد"),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("المبلغ"),
    )
    payment_date = models.DateField(
        default=now,
        verbose_name=_("تاريخ الدفع"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("الوصف"),
    )

    def __str__(self):
        return f"دفع: {self.amount} للعقد {self.contract}"

    class Meta:
        verbose_name = _("دفع")
        verbose_name_plural = _("المدفوعات")
        ordering = ["-payment_date"]
        indexes = [
            models.Index(fields=["payment_date"]),
        ]

class Reminder(AbstractBaseModel):
  tenant = models.ForeignKey(
    Tenant,
    on_delete=models.CASCADE,
    related_name="reminders",
    verbose_name=_("المستأجر"),
  )
  contract = models.ForeignKey(
    LeaseContract,
    on_delete=models.CASCADE,
    blank=True,
    null=True,
    related_name="reminders",
    verbose_name=_("العقد"),
  )
  message = models.TextField(
    verbose_name=_("رسالة التذكير"),
  )
  is_sent = models.BooleanField(
    default=False,
    verbose_name=_("تم الإرسال"),
  )

  def send_notification(self):
    if not self.is_sent:
      print(f"إرسال تذكير إلى {self.tenant.full_name}: {self.message}")
      self.is_sent = True
      self.save()

  def __str__(self):
    return f"تذكير للمستأجر: {self.tenant.full_name}"

  class Meta:
    verbose_name = _("تذكير")
    verbose_name_plural = _("التذكيرات")
    ordering = ["-created_at"]
    indexes = [
        models.Index(fields=["is_sent"]),
    ]
      
class Notification(AbstractBaseModel):
    message = models.TextField(
        verbose_name=_("الرسالة"),
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name=_("مقروء"),
    )
    priority = models.CharField(
        max_length=50,
        choices=(
            ('low', _('منخفضة')),
            ('medium', _('متوسطة')),
            ('high', _('عالية')),
        ),
        default='low',
        verbose_name=_("الأولوية"),
    )

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"إشعار: {self.message[:20]}"

    class Meta:
        verbose_name = _("إشعار")
        verbose_name_plural = _("الإشعارات")
        ordering = ["-created_at"]

class MaintenanceRequest(AbstractBaseModel):
  unit = models.ForeignKey(
    Unit,
    on_delete=models.CASCADE,
    related_name="maintenance_requests",
    verbose_name=_("الوحدة"),
  )
  description = models.TextField(
    verbose_name=_("وصف المشكلة"),
  )
  request_date = models.DateField(
    default=now,
    verbose_name=_("تاريخ الطلب"),
  )
  priority = models.CharField(
    max_length=50,
    choices=(
      ('low', _('منخفضة')),
      ('medium', _('متوسطة')),
      ('high', _('عالية')),
    ),
    default='low',
    verbose_name=_("الأولوية"),
  )
  is_resolved = models.BooleanField(
    default=False,
    verbose_name=_("تمت المعالجة"),
  )

  def __str__(self):
    return f"طلب الصيانة: {self.unit.number}"

  class Meta:
    verbose_name = _("طلب الصيانة")
    verbose_name_plural = _("طلبات الصيانة")
    ordering = ["-request_date"]

class MaintenanceFeedback(AbstractBaseModel):
  maintenance_requests = models.OneToOneField(
    MaintenanceRequest,
    on_delete=models.CASCADE,
    related_name="feedbacks",
    verbose_name=_("طلب الصيانة"),
  )
  rating = models.PositiveIntegerField(
    default=5,
    verbose_name=_("التقييم"),
  )
  comments = models.TextField(
    blank=True,
    null=True,
    verbose_name=_("التعليقات"),
  )

  def __str__(self):
    return f"تقييم صيانة: {self.maintenance_requests.unit.number}"

  class Meta:
    verbose_name = _("تقييم صيانة")
    verbose_name_plural = _("تقييمات الصيانة")
    ordering = ["-created_at"]

class Report(AbstractBaseModel):
  name = models.CharField(
    max_length=200,
    verbose_name=_("اسم التقرير"),
  )
  report_type = models.CharField(
    max_length=100,
    verbose_name = _("نوع التقرير"),
  )
  content = models.TextField(
    verbose_name=_("محتوى التقرير"),
  )
  generated_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name=_("تاريخ الإنشاء"),
  )

  def __str__(self):
    return f"تقرير: {self.name}"

  class Meta:
    verbose_name = _("تقرير")
    verbose_name_plural = _("التقارير")
    ordering = ["-generated_at"]

class LatePayment(AbstractBaseModel):
    invoice = models.OneToOneField(
        "Invoice",
        on_delete=models.CASCADE,
        related_name="late_payment",
        verbose_name=_("الفاتورة"),
    )
    days_late = models.PositiveIntegerField(
        verbose_name=_("عدد الأيام المتأخرة"),
    )
    penalty = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("غرامة التأخير"),
    )

    def calculate_penalty(self, daily_rate=5):
      self.penalty = self.days_late * daily_rate
      self.save()

    def __str__(self):
        return f"غرامة - {self.invoice.contract.unit.number}"

    class Meta:
        verbose_name = _("غرامة تأخير")
        verbose_name_plural = _("غرامات التأخير")
        ordering = ["-created_at"]

class SystemSettings(AbstractBaseModel):
    key = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_("اسم الإعداد"),
    )
    value = models.TextField(
        verbose_name=_("القيمة"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("الوصف"),
    )

    def __str__(self):
        return f"إعداد: {self.key}"

    class Meta:
        verbose_name = _("إعداد النظام")
        verbose_name_plural = _("إعدادات النظام")
        ordering = ["key"]