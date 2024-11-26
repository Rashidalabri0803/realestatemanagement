# Generated by Django 5.0.2 on 2024-11-25 16:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_management', '0003_alter_tenantbankaccount_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifiction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='الرسالة')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('is_read', models.BooleanField(default=False, verbose_name='مقروء')),
            ],
            options={
                'verbose_name': 'إشعار',
                'verbose_name_plural': 'الإشعارات',
            },
        ),
        migrations.AddField(
            model_name='tenant',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='ملاحظات'),
        ),
        migrations.CreateModel(
            name='LeaseContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='تاريخ البدء')),
                ('end_date', models.DateField(verbose_name='تاريخ الانتهاء')),
                ('monthly_rent', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='الإيجار الشهري')),
                ('is_active', models.BooleanField(default=True, verbose_name='نشط')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.tenant', verbose_name='المستأجر')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.unit', verbose_name='الوحدة')),
            ],
            options={
                'verbose_name': 'عقد إيجار',
                'verbose_name_plural': 'عقود الايجار',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='المبلغ')),
                ('payment_date', models.DateField(verbose_name='تاريخ الدفع')),
                ('description', models.TextField(blank=True, null=True, verbose_name='الوصف')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental_management.leasecontract', verbose_name='العقد')),
            ],
        ),
    ]
