from django.contrib import admin

from .models import (
    Building,
    Expense,
    MaintenanceRequest,
    RentReport,
    Tenant,
    TenantBankAccount,
    Unit,
)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created_at', 'updated_at', 'image_preview')
    search_fields = ('name', 'address')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at' , 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return "<img src='{obj.image.url}' width='50' height='50' />"
        return "لا توجد صورة"
    image_preview.allow_tags = True
    image_preview.short_description = 'صورة المبني'

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('number', 'building', 'unit_type', 'status', 'monthly_rent', 'image_preview')
    list_filter = ('unit_type', 'status', 'building')
    search_fields = ('number', 'building__name')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return f"<img src='{obj.image.url}' width='50' height='50' />"
        return "لا توجد صورة"
    image_preview.allow_tags = True
    image_preview.short_description = 'صورة الوحدة'
    
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email')
    search_fields = ('full_name', 'phone_number', 'email')
    list_filter = ('full_name',)

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('unit', 'description', 'request_date', 'is_resolved', 'resolved_date')
    list_filter = ('is_resolved', 'request_date', 'resolved_date')
    search_fields = ('unit__number', 'description')
    readonly_fields = ('request_date',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('building', 'description', 'amount', 'date')
    list_filter = ('building', 'date')
    search_fields = ('description', 'building__name')

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