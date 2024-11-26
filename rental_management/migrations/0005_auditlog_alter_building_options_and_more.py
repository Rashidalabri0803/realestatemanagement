# Generated by Django 5.0.3 on 2024-11-26 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_management', '0004_notifiction_tenant_description_leasecontract_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=200, verbose_name='الإجراء')),
                ('model_name', models.CharField(max_length=200, verbose_name='اسم النموذج')),
                ('object_id', models.PositiveIntegerField(verbose_name='معرف العنصر')),
                ('user', models.CharField(max_length=200, verbose_name='المستخدم')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإجراء')),
                ('details', models.TextField(blank=True, null=True, verbose_name='تفاصيل')),
            ],
            options={
                'verbose_name': 'سجل',
                'verbose_name_plural': 'السجلات',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AlterModelOptions(
            name='building',
            options={'ordering': ['name'], 'verbose_name': 'مبنى', 'verbose_name_plural': 'المباني'},
        ),
        migrations.AlterModelOptions(
            name='leasecontract',
            options={'ordering': ['-start_date'], 'verbose_name': 'عقد إيجار', 'verbose_name_plural': 'عقود الايجار'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'دفعة', 'verbose_name_plural': 'الدفعات'},
        ),
        migrations.AlterField(
            model_name='unit',
            name='status',
            field=models.CharField(choices=[('Available', 'متاحة'), ('Rented', 'مؤجرة'), ('Maintenance', 'تحت الصيانة')], default='Available', max_length=50, verbose_name='الحالة'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unit_type',
            field=models.CharField(choices=[('Office', 'مكتب'), ('Apartment', 'شقة'), ('Shop', 'محل')], max_length=50, verbose_name='نوع الوحدة'),
        ),
        migrations.AddIndex(
            model_name='unit',
            index=models.Index(fields=['status', 'unit_type'], name='rental_mana_status_0c2f54_idx'),
        ),
    ]
