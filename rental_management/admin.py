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
    Notifiction,
    Attachment,
    AuditLog,
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
    list_display = ('full_name', 'phone_number', 'email', 'active_contracts', 'overdue_payments', 'profile_picture_preview')
    search_fields = ('full_name', 'phone_number', 'email')
    readonly_fields = ('profile_picture_preview',)

    def active_conracts(self, obj):
        return obj.active_contracts()
    active_conracts.short_description = 'العقود النشطة'

    def overdue_payments(self, obj):
        return obj.overdue_payments()
    overdue_payments.short_description = 'الدفعات المتأخرة'
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(f'<img src="{obj.profile_picture.url}" width="50" height="50" />')
        return "لا توجد صورة"
    profile_picture_preview.short_description = 'صورة المستأجر'
    
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
        return "نعم" if obj.is_due_soon() else "لا"
    is_due_soon.short_description = 'سينتهي قريبا'
    is_due_soon.boolean = True

    @admin.action(description='تعيين العقود كمنتهية')
    def mark_contracts_terminated(self, request, queryset):
        queryset.update(is_active=False)
        self.messege_user(queryset, f'تم إنهاء {queryset.count()} عقد بنجاح. ')

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('description', 'file', 'description')
    search_fields = ('contract__id', 'description')
    readonly_fields = ('file_preview',)

    def file_preview(self, obj):
        if obj.file:
            return format_html(f"<a href="{obj.file.url}" target='_blank'>عرض الملف</a>")
        return "لا توجد ملفات"
    file_preview.short_description = 'عرض الملف'

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
        self.messege_user(queryset, f'تم معالجة {queryset.count()} طلب بنجاح. ')

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
        self.messege_user(queryset, f'تم تحديد {queryset.count()} إشعار كمقروء. ')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'model_name', 'user', 'timestamp', 'details')
    list_filter = ('model_name', 'timestamp')
    search_fields = ('action', 'model_name', 'user', 'details')
    readonly_fields = ('timestamp',)