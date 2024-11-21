from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=200, verbose_name='اسم المبني')
    address = models.TextField(verbose_name='عنوان المبني')
    description = models.TextField(blank=True, null=True, verbose_name='وصف')

    def __str__(self):
        return self.name

class Units(models.Model):
  UNIT_TYPE_CHOICES = [
    ('office', 'مكتب'),
    ('apartment', 'شقة'),
    ('shope', 'متجر')
  ]
  building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name='المبني')
  unit_type = models.CharField(max_length=50, choices=UNIT_TYPE_CHOICES, verbose_name='نوع الوحدة')
  number = models.CharField(max_length=50, verbose_name='رقم الوحدة')
  area = models.FloatField(verbose_name='المساحة (متر مربع)')
  monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='الإيجار الشهري')

  def __str__(self):
    return f'{self.unit_type} - {self.number}'

class Tenant(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='الاسم الكامل')
    phone_number = models.CharField(max_length=200, verbose_name='رقم الهاتف')
    email = models.EmailField(blank=True, null=True, verbose_name='البريد الإلكتروني')

    def __str__(self):
        return self.full_name

class LeaseContract(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='المستأجر')
    unit = models.ForeignKey(Units, on_delete=models.CASCADE, verbose_name='الوحدة')
    start_date = models.DateField(verbose_name='تاريخ بدء العقد')
    end_date = models.DateField(verbose_name='تاريخ انتهاء العقد')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='إجمالي قيمة العقد')
    is_active = models.BooleanField(default=True, verbose_name='العقد نط')

    def __str__(self):
        return f'عقد إيجار: {self.tenant} - {self.unit}'