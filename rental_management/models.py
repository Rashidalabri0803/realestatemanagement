from django.db import models
from django.utils.translation import gettext_lazy as _


# نموذج المباني
class Building(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("اسم المبنى"))
    address = models.TextField(verbose_name=_("عنوان المبنى"))
    description = models.TextField(blank=True, null=True, verbose_name=_("وصف"))
    image = models.ImageField(upload_to='building_images/', blank=True, null=True, verbose_name=_("صورة المبنى"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإنشاء"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاريخ التحديث"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("مبنى")
        verbose_name_plural = _("المباني")


# نموذج الوحدات
class Unit(models.Model):
    UNIT_TYPE_CHOICES = [
        ('office', _("مكتب")),
        ('apartment', _("شقة")),
        ('shop', _("محل")),
    ]
    UNIT_STATUS_CHOICES = [
        ('available', _("متاحة")),
        ('rented', _("مؤجرة")),
        ('maintenance', _("تحت الصيانة")),
    ]

    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name=_("المبنى"))
    unit_type = models.CharField(max_length=50, choices=UNIT_TYPE_CHOICES, verbose_name=_("نوع الوحدة"))
    status = models.CharField(max_length=50, choices=UNIT_STATUS_CHOICES, default='available', verbose_name=_("الحالة"))
    number = models.CharField(max_length=50, verbose_name=_("رقم الوحدة"))
    area = models.FloatField(verbose_name=_("المساحة (م²)"))
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("الإيجار الشهري"))
    image = models.ImageField(upload_to='unit_images/', blank=True, null=True, verbose_name=_("صورة الوحدة"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإنشاء"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاريخ التحديث"))

    def __str__(self):
        return f"{self.get_unit_type_display()} - {self.number}"

    class Meta:
        verbose_name = _("وحدة")
        verbose_name_plural = _("الوحدات")


# نموذج المستأجرين
class Tenant(models.Model):
    full_name = models.CharField(max_length=200, verbose_name=_("الاسم الكامل"))
    phone_number = models.CharField(max_length=20, verbose_name=_("رقم الهاتف"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("البريد الإلكتروني"))
    description = models.TextField(blank=True, null=True, verbose_name=_("ملاحظات"))

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _("مستأجر")
        verbose_name_plural = _("المستأجرون")


# نموذج طلبات الصيانة
class MaintenanceRequest(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name=_("الوحدة"))
    description = models.TextField(verbose_name=_("تفاصيل المشكلة"))
    request_date = models.DateField(verbose_name=_("تاريخ الطلب"))
    is_resolved = models.BooleanField(default=False, verbose_name=_("تمت معالجتها"))
    resolved_date = models.DateField(blank=True, null=True, verbose_name=_("تاريخ المعالجة"))

    def __str__(self):
        return f"طلب صيانة - {self.unit.number}"

    class Meta:
        verbose_name = _("طلب صيانة")
        verbose_name_plural = _("طلبات الصيانة")


# نموذج المصاريف
class Expense(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name=_("المبنى"))
    description = models.TextField(verbose_name=_("وصف المصروف"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("المبلغ"))
    date = models.DateField(verbose_name=_("تاريخ المصروف"))

    def __str__(self):
        return f"{self.description} - {self.amount}"

    class Meta:
        verbose_name = _("مصروف")
        verbose_name_plural = _("المصاريف")


# نموذج الحساب البنكي للمستأجر
class TenantBankAccount(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, verbose_name=_("المستأجر"))
    bank_name = models.CharField(max_length=100, verbose_name=_("اسم البنك"))
    account_number = models.CharField(max_length=50, verbose_name=_("رقم الحساب"))
    iban = models.CharField(max_length=34, verbose_name=_("رقم الآيبان"))

    def __str__(self):
        return f"حساب {self.tenant.full_name}"

    class Meta:
        verbose_name = _("حساب بنكي")
        verbose_name_plural = _("الحسابات البنكية")


# نموذج تقارير الإيجار
class RentReport(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name=_("المبنى"))
    total_income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("إجمالي الدخل"))
    generated_date = models.DateField(auto_now_add=True, verbose_name=_("تاريخ التقرير"))

    def __str__(self):
        return f"تقرير دخل {self.building.name}"

    class Meta:
        verbose_name = _("تقرير الإيجار")
        verbose_name_plural = _("تقارير الإيجار")
