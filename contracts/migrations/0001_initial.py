# Generated by Django 5.0.3 on 2025-01-03 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_name', models.CharField(max_length=255, verbose_name='اسم المستأجر')),
                ('start_date', models.DateField(verbose_name='تاريخ البداية')),
                ('end_date', models.DateField(verbose_name='تاريخ النهاية')),
                ('terms', models.TextField(blank=True, null=True, verbose_name='الشروط العقد')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property', verbose_name='الوحدة')),
            ],
        ),
    ]