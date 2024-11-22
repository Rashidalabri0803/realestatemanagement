# Generated by Django 5.0.3 on 2024-11-24 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='اسم المبني')),
                ('address', models.CharField(max_length=200, verbose_name='عنوان المبني')),
                ('description', models.TextField(blank=True, null=True, verbose_name='وصف')),
                ('image', models.ImageField(blank=True, null=True, upload_to='building_images/', verbose_name='صورة المبني')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
            ],
            options={
                'verbose_name': 'مبنى',
                'verbose_name_plural': 'المباني',
            },
        ),
        migrations.CreateModel(
            name='LeaseContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='تاريخ بدء العقد')),
                ('end_date', models.DateField(verbose_name='تاريخ انتهاء العقد')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='إجمالي قيمة العقد')),
                ('is_active', models.BooleanField(default=True, verbose_name='العقد نط')),
                ('document', models.FileField(blank=True, null=True, upload_to='contracts/', verbose_name='مستند العقد')),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name='الاسم الكامل')),
                ('phone_number', models.CharField(max_length=200, verbose_name='رقم الهاتف')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='البريد الإلكتروني')),
                ('description', models.TextField(blank=True, null=True, verbose_name='ملاحظات')),
            ],
            options={
                'verbose_name': 'مستأجر',
                'verbose_name_plural': 'المستأجرون',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='وصف المصروف')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='المبلغ')),
                ('date', models.DateField(verbose_name='تاريخ المصروف')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.building', verbose_name='المبني')),
            ],
            options={
                'verbose_name': 'مصروف',
                'verbose_name_plural': 'المصاريف',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_due', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='المبلغ المستحق')),
                ('due_date', models.DateField(verbose_name='تاريخ الاستحقاق')),
                ('is_paid', models.BooleanField(default=False, verbose_name='مدفوع')),
                ('payment_date', models.DateField(blank=True, null=True, verbose_name='تاريخ الدفع')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.leasecontract', verbose_name='العقد')),
            ],
        ),
        migrations.CreateModel(
            name='RentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_income', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='إجمالي الدخل')),
                ('generated_date', models.DateField(auto_now_add=True, verbose_name='تاريخ التقرير')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.building', verbose_name='المبني')),
            ],
            options={
                'verbose_name': 'تقرير إيجار',
                'verbose_name_plural': 'تقارير الإيجار',
            },
        ),
        migrations.AddField(
            model_name='leasecontract',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.tenant', verbose_name='المستأجر'),
        ),
        migrations.CreateModel(
            name='TenantBankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=200, verbose_name='اسم البنك')),
                ('account_number', models.CharField(max_length=200, verbose_name='رقم الحساب')),
                ('iban', models.CharField(max_length=200, verbose_name='رقم الايبان')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.tenant', verbose_name='المستأجر')),
            ],
            options={
                'verbose_name': 'حساب بنكي',
                'verbose_name_plural': 'الحسابات البنكية',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_type', models.CharField(choices=[('avaliable', 'متاحة'), ('rented', 'مؤجرة'), ('maintenance', 'تحت الصيانة')], max_length=50, verbose_name='نوع الوحدة')),
                ('status', models.CharField(choices=[('avaliable', 'متاحة'), ('rented', 'مؤجرة'), ('maintenance', 'تحت الصيانة')], default='available', max_length=50, verbose_name='الحالة')),
                ('number', models.CharField(max_length=50, verbose_name='رقم الوحدة')),
                ('area', models.FloatField(verbose_name='المساحة (متر مربع)')),
                ('monthly_rent', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='الإيجار الشهري')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.building', verbose_name='المبني')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='تفاصيل المشكلة')),
                ('request_date', models.DateField(auto_now_add=True, verbose_name='تاريخ الطلب')),
                ('is_resolved', models.BooleanField(default=False, verbose_name='تمت معالجتها')),
                ('resolved_date', models.DateField(blank=True, null=True, verbose_name='تاريخ المعالجة')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.unit', verbose_name='الوحدة')),
            ],
            options={
                'verbose_name': 'طلب صيانة',
                'verbose_name_plural': 'طلبات الصيانة',
            },
        ),
        migrations.AddField(
            model_name='leasecontract',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.unit', verbose_name='الوحدة'),
        ),
    ]
