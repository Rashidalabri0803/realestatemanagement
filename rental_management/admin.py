from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Building,
    Unit,
    Tenant,
    LeaseContract,
    Payment,
    MaintenanceRequest,
    Expense,
    Notification,
    AuditLog,
    Invoice,
    Reminder,
    Subscription,
    Report,
)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'total_units', 'total_rent', 'yearly_rent', 'image_preview', 'created_at')
    search_fields = ('name', 'address')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at' , 'image_preview')

    def total_units(self, obj):
        return obj.unit_set.count()
    total_units.short_description = 'إجمالي الوحدات'

    def total_rent(self, obj):
        return obj.total_rent()
    total_rent.short_description = 'الإيجار الشهري'

    def yearly_rent(self, obj):
        return obj.yearly_rent()
    yearly_rent.short_description = 'الإيجار السنوي'

    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "لا توجد صورة"
    image_preview.short_description = 'صورة المبني'

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('number', 'building', 'unit_type', 'status', 'monthly_rent', 'yearly_rent', 'image_preview')
    search_fields = ('number', 'building__name')
    list_filter = ('status', 'unit_type',  'building')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')

    def yearly_rent(self, obj):
        return obj.yearly_rent()
    yearly_rent.short_description = 'الإيجار السنوي'

    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "لا توجد صورة"
    image_preview.short_description = 'صورة الوحدة'

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'is_active', 'created_at')
    search_fields = ('full_name', 'email')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

    def active_contracts(self, obj):
        return obj.active_contracts()
    active_contracts.short_description = 'العقود النشطة'

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(f'<img src="{obj.profile_picture.url}" width="50" height="50" />')
        return "لا توجد صورة"
        
@admin.register(LeaseContract)
class LeaseContractAdmin(admin.ModelAdmin):
    list_display = ('unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'is_active', 'remaining_days', 'is_due_soon')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('unit__number', 'tenant__full_name')
    readonly_fields = ('remaining_days',)
    actions = ['mark_contracts_terminated']
    
    def remaining_days(self, obj):
        days = obj.remaining_days()
        if days is not None:
            return f'{days} يوم' if days > 0 else 'منتهي'
        return 'غير محدد'
    remaining_days.short_description = 'الأيام المتبقية'

    def is_due_soon(self, obj):
        return obj.is_due_soon()
    is_due_soon.short_description = 'سينتهي قريبا'
    is_due_soon.boolean = True

    @admin.action(description='تحديد العقود كمنتهية')
    def mark_contracts_terminated(self, request, queryset):
        queryset.update(is_active=False)
        self.messege_user(queryset, f'تم إنهاء {queryset.count()} عقد بنجاح. ')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'tenant', 'building', 'total_rent', 'total_payments', 'total_expenses', 'total_amount', 'is_paid', 'created_at')
    search_fields = ('number', 'tenant__full_name', 'building__name')
    list_filter = ('is_paid', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

    def days_until_dues(self, obj):
        return obj.days_until_dues()
    days_until_dues.short_description = 'الأيام المتبقية'

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'is_sent', 'created_at')
    search_fields = ('tenant__full_name', 'tenant__email')
    list_filter = ('is_sent', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'building', 'is_active', 'created_at')
    search_fields = ('tenant__full_name', 'building__name')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

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
        self.messege_user(queryset, f'تم معالجة {queryset.count()} طلب بنجاح. ')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'last_generated')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'last_generated')
    readonly_fields = ('created_at', 'last_generated')

    def generate_report(self, request, queryset):
        for report in queryset:
            report.generate_report()
        self.messege_user(queryset, f'تم توليد التقارير بنجاح. ')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'model_name', 'user', 'timestamp', 'details')
    list_filter = ('model_name', 'timestamp')
    search_fields = ('action', 'model_name', 'user', 'details')
    readonly_fields = ('timestamp',)
    
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('building', 'description', 'amount', 'date')
    list_filter = ('building', 'date')
    search_fields = ('description', 'building__name')