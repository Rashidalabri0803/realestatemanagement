from django.contrib import admin

from .models import (
    Building,
    Invoice,
    LatePayment,
    LeaseContract,
    MaintenanceFeedback,
    MaintenanceRequest,
    Notification,
    Reminder,
    Report,
    SystemSettings,
    Tenant,
    Unit,
)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'total_units', 'rented_units', 'rented_percentage', 'monthly_income')
    search_fields = ('name', 'address')
    list_filter = ('created_at', 'updated_at')
    actions = ['export_to_csv']

    @admin.action(description='تصدير المباني إلى ملف CSV')
    def export_to_csv(self, request, queryset):
        import csv

        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="buildings.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Address', 'Total Units', 'Rented Units', 'Monthly Income'])

        for building in queryset:
            writer.writerow([
              building.id, building.name, building.address,
              building.total_units(), building.rented_units(), building.monthly_income()])
        return response
      
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('building', 'number', 'unit_type', 'status', 'monthly_rent', 'is_available')
    search_fields = ('building__name', 'number')
    list_filter = ('building', 'unit_type', 'status')
  
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'id_card', 'active_contracts_count', 'total_payments')
    search_fields = ('full_name', 'phone_number', 'email')
    list_filter = ('created_at',)
  
@admin.register(LeaseContract)
class LeaseContractAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'unit', 'start_date', 'end_date', 'monthly_rent', 'is_active', 'remaining_days')
    search_fields = ('tenant__full_name', 'unit__number')
    list_filter = ('start_date', 'end_date', 'is_active')
  
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('contract', 'issue_date', 'due_date', 'amount', 'is_paid', 'late_fee', 'is_overdue')
    search_fields = ('contract__tenant__full_name', 'contract__unit__number')
    list_filter = ('due_date', 'is_paid')
  
@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'contract', 'message', 'is_sent', 'created_at')
    search_fields = ('tenant__full_name', 'contract__unit__number')
    list_filter = ('created_at', 'is_sent')
  
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'priority', 'is_read', 'created_at')
    search_fields = ('message',)
    list_filter = ('priority', 'is_read')
  
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
  
    list_display = ('unit', 'description', 'priority', 'is_resolved', 'request_date')
    search_fields = ('unit__number', 'description',)
    list_filter = ('priority', 'is_resolved', 'request_date')
  
@admin.register(MaintenanceFeedback)
class MaintenanceFeedbackAdmin(admin.ModelAdmin):
    list_display = ('maintenance_requests', 'rating', 'comments', 'created_at')
    search_fields = ('maintenance_requests__unit__number', 'comments')
    list_filter = ('created_at', 'rating')
@admin.register(LatePayment)
class LatePaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'days_late', 'penalty', 'created_at')
    search_fields = ('invoice__contract__tenant__full_name', 'invoice__contract__unit__number')
    list_filter = ('created_at',)
  
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'generated_at')
    search_fields = ('name', 'report_type')
    list_filter = ('generated_at',)
  
@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
    search_fields = ('key', 'value', 'description')
    list_filter = ('created_at',)