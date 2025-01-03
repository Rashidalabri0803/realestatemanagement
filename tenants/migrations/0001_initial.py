# Generated by Django 5.0.3 on 2025-01-03 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='الاسم')),
                ('phone', models.CharField(max_length=15, verbose_name='رقم الهاتف')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='البريد الإلكتروني')),
                ('address', models.TextField(verbose_name='العنوان')),
            ],
            options={
                'verbose_name': 'مستأجر',
                'verbose_name_plural': 'المستأجرون',
            },
        ),
    ]