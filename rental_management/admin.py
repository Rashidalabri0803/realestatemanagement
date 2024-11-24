from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Building,
    Expense,
    MaintenanceRequest,
    RentReport,
    Tenant,
    TenantBankAccount,
    Unit,
    LeaseContract,
    Payment,
    Notifiction,
)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created_at', 'updated_at', 'image_preview')
    search_fields = ('name', 'address')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at' , 'image_preview')

    def total_units(self, obj):
        return obj.unit_set.count()
    total_units.short_description = 'إجمالي الوحدات'

    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "لا توجد صورة"
    image_preview.short_description = 'صورة المبني'

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('number', 'building', 'unit_type', 'status', 'monthly_rent', 'image_preview')
    list_filter = ('unit_type', 'status', 'building')
    search_fields = ('number', 'building__name')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "لا توجد صورة"
    image_preview.short_description = 'صورة الوحدة'
    
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email')
    search_fields = ('full_name', 'phone_number', 'email')
    list_filter = ('full_name',)

@admin.register(LeaseContract)
class LeaseContractAdmin(admin.ModelAdmin):
    list_display = ('unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'is_active', 'remaining_days')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('unit__number', 'tenant__full_name')

    def remaining_days(self, obj):
        days = obj.remaining_days()
        if days is not None:
            return f'{days} يوم' if days > 0 else 'منتهي'
        return 'غير محدد'
    remaining_days.short_description = 'الأيام المتبقية'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('contract', 'amount', 'payment_date', 'description')
    list_filter = ('payment_date',)
    search_fields = ('contract__unit__number', 'contract__tenant__full_name')
    
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('unit', 'description', 'request_date', 'is_resolved', 'resolved_date')
    list_filter = ('is_resolved', 'request_date', 'resolved_date')
    search_fields = ('unit__number', 'description')
    readonly_fields = ('request_date',)
    actions = ['mark_as_resolved']

    @admin.action(description='تحديد الطلبات كمعالجة')
    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('building', 'description', 'amount', 'date')
    list_filter = ('building', 'date')
    search_fields = ('description', 'building__name')

@admin.register(Notifiction)
class NotifictionAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message',)
    actions = ['mark_as_read']

    @admin.action(description='تحديد الإشعارات كمقروءة')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        
@admin.register(TenantBankAccount)
class TenantBankAccountAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'bank_name', 'account_number', 'iban')
    search_fields = ('tenant__full_name', 'bank_name', 'account_number', 'iban')

@admin.register(RentReport)
class RentReportAdmin(admin.ModelAdmin):
    list_display = ('building', 'total_income', 'generated_date')
    list_filter = ('building', 'generated_date')
    search_fields = ('building__name',)
    readonly_fields = ('generated_date',)