from rest_framework import serializers
from .models import Building, Unit,Tenant, LeaseContract, Invoice, Payment, Reminder, Notification, MaintenanceRequest, MaintenanceFeedback, LatePayment, Report, SystemSettings

class BuildingSerializer(serializers.ModelSerializer):
    total_units = serializers.IntegerField(read_only=True)
    rented_units = serializers.IntegerField(read_only=True)
    rented_percentage = serializers.FloatField(read_only=True)
    monthly_income = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Building
        fields = [
            'id',
            'name',
            'description',
            'image',
            'total_units',
            'rented_units',
            'rented_percentage',
            'monthly_income',
        ]

class UnitSerializer(serializers.ModelSerializer):
  is_available = serializers.BooleanField(read_only=True)

  class Meta:
    model = Unit
    fields = [
      'id',
      'number',
      'building',
      'unit_type',
      'status',
      'number',
      'area',
      'monthly_rent',
      'is_available',
    ]

class TenantSerializer(serializers.ModelSerializer):
  active_contracts_count = serializers.IntegerField(read_only=True)
  total_payments = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
  class Meta:
    model = Tenant
    fields = [
      'id',
      'full_name',
      'phone_number',
      'email',
      'id_card',
      'profile_picture',
      'active_contracts_count',
      'total_payments',
    ]

class LeaseContractSerializer(serializers.ModelSerializer):
  remaining_days = serializers.IntegerField(read_only=True)
  class Meta:
    model = LeaseContract
    fields = [
      'id',
      'unit',
      'tenant',
      'start_date',
      'end_date',
      'monthly_rent',
      'is_active',
      'remaining_days',
    ]

class InvoiceSerializer(serializers.ModelSerializer):
  late_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
  is_overdue = serializers.BooleanField(read_only=True)
  
  class Meta:
    model = Invoice
    fields = [
      'id',
      'contract',
      'issue_date',
      'due_date',
      'amount',
      'is_paid',
      'late_fee',
      'is_overdue',
    ]

class PaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Payment
    fields = [
      'id',
      'contract',
      'amount',
      'payment_date',
      'descripition',
    ]

class ReminderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reminder
    fields = [
      'id',
      'tenant',
      'contract',
      'message',
      'is_sent',
      'created_at',
    ]

class NotificationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Notification
    fields = [
      'id',
      'message',
      'is_read',
      'priority',
      'created_at',
    ]

class MaintenanceRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = MaintenanceRequest
    fields = [
      'id',
      'unit',
      'description',
      'request_date',
      'priority',
      'is_resolved',
    ]

class MaintenanceFeedbackSerializer(serializers.ModelSerializer):
  class Meta:
    model = MaintenanceFeedback
    fields = [
      'id',
      'mainteance_request',
      'rating',
      'comments',
      'created_at',
    ]

class LatePaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model = LatePayment
    fields = [
      'id',
      'invoice',
      'days_late',
      'penalty',
      'created_at',
    ]

class ReportSerializer(serializers.ModelSerializer):
  class Meta:
    model = Report
    fields = [
      'id',
      'name',
      'report_type',
      'content',
      'generated_at',
    ]

class SystemSettingsSerializer(serializers.ModelSerializer):
  class Meta:
    model = SystemSettings
    fields = [
      'id',
      'key',
      'value',
      'description',
      'created_at'
    ]