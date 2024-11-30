from django.contrib import admin

from .models import (
    AnnualRentDetail,
    AuditLog,
    Building,
    DailyPaymentLog,
    Feedback,
    Invoice,
    LatePaymnet,
    LeaseContract,
    MaintenanceFeedback,
    MaintenanceRequest,
    MessageLog,
    Notification,
    Payment,
    Reminder,
    ReminderLog,
    Report,
    ScheduledReminder,
    Subscription,
    SystemEvent,
    SystemSettings,
    SystemStatistics,
    Tenant,
    Unit,
    UserProfile,
    UserRole,
)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'total_units', 'rented_units', 'rented_percentage')
    search_fields = ('name', 'address')
    list_filter = ('name',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('number', 'building', 'unit_type', 'status','monthly_rent')
    search_fields = ('number', 'building__name')
    list_filter = ('unit_type', 'status', 'building',)

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'id_card')
    search_fields = ('full_name', 'phone_number', 'email')
    list_filter = ('full_name',)

@admin.register(LeaseContract)
class LeaseContractAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'unit', 'start_date', 'end_date', 'monthly_rent', 'is_active')
    search_fields = ('tenant__full_name', 'unit__number')
    list_filter = ('is_active',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('contract', 'issue_date', 'due_date', 'amount', 'is_paid', 'late_fee')
    search_fields = ('contract__tenant__full_name', 'contract__unit__number')
    list_filter = ('is_paid', 'due_date',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('contract', 'amount', 'payment_date', 'status')
    search_fields = ('contract__tenant__full_name', 'contract__unit__number')
    list_filter = ('status', 'payment_date',)

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'contract', 'message', 'is_sent', 'created_at')
    search_fields = ('tenant__full_name', 'contract__unit__number')
    list_filter = ('is_sent', 'created_at',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'is_read', 'priority', 'related_model', 'created_at')
    search_fields = ('message',)
    list_filter = ('is_read', 'priority',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'model_name', 'user', 'ip_address', 'timestamp')
    search_fields = ('action', 'model_name', 'user')
    list_filter = ('action', 'timestamp',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'generated_at', 'is_scheduled')
    search_fields = ('name', 'report_type')
    list_filter = ('is_scheduled', 'generated_at',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'service_name', 'service_type', 'monthly_fee', 'start_date', 'end_date', 'is_active')
    search_fields = ('tenant__full_name', 'service_name')
    list_filter = ('service_type', 'is_active',)

@admin.register(LatePaymnet)
class LatePaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'days_late', 'penalty', 'created_at')
    search_fields = ('invoice__contract__tenant__full_name', 'invoice__contract__unit__number')
    list_filter = ('created_at',)

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('unit', 'description', 'priorty', 'is_resolved', 'request_date')
    search_fields = ('unit__number', 'description')
    list_filter = ('priorty', 'is_resolved', 'request_date',)

@admin.register(MaintenanceFeedback)
class MaintenanceFeedbackAdmin(admin.ModelAdmin):
    list_display = ('maintenance_request', 'rating', 'comments', 'created_at')
    search_fields = ('maintenance_request__unit__number', 'comments')
    list_filter = ('rating', 'created_at',)

@admin.register(AnnualRentDetail)
class AnnualRentDetailAdmin(admin.ModelAdmin):
    list_display = ('unit', 'year', 'total_rent', 'paid_amount', 'outstanding_amount')
    search_fields = ('unit__number',)
    list_filter = ('year',)

@admin.register(SystemEvent)
class SystemEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'description', 'timestamp')
    search_fields = ('description',)
    list_filter = ( 'event_type', 'timestamp',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'unit', 'comment', 'rating', 'created_at')
    search_fields = ('tenant__full_name', 'unit__number', 'comment')
    list_filter = ('rating', 'created_at',)

@admin.register(DailyPaymentLog)
class DailyPaymentLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_payments', 'total_invoices', 'total_late_payments')
    search_fields = ('date',)
    list_filter = ('date',)

@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
    list_display = ('reminder', 'sent_date', 'status', 'response_message')
    search_fields = ('reminder__tenant__full_name', 'status')
    list_filter = ('status', 'sent_date',)

@admin.register(ScheduledReminder)
class ScheduledReminderAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'contract', 'scheduled_date', 'is_sent')
    search_fields = ('tenant__full_name', 'contract__unit__number')
    list_filter = ('is_sent', 'scheduled_date',)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number', 'address')
    search_fields = ('user__username', 'role__name', 'phone_number')

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
    search_fields = ('key', 'description')

@admin.register(SystemStatistics)
class SystemStatisticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_buildings', 'total_units', 'total_tenants', 'total_income')
    search_fields = ('date',)
    list_filter = ('date',)

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'sent_date', 'status', 'response_details')
    search_fields = ('recipient', 'message', 'status')
    list_filter = ('status', 'sent_date',)