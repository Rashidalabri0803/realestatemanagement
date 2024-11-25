from rest_framework import serializers

from .models import (
    Building,
    Expense,
    MaintenanceRequest,
    RentReport,
    Tenant,
    TenantBankAccount,
    Unit,
)


class BuildingSerializer(serializers.ModelSerializer):
    total_units = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Building
        fields = ('id', 'name', 'address', 'total_units', 'image_url')

    def get_total_units(self, obj):
        return obj.units.count()

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

class UnitSerializer(serializers.ModelSerializer):
    building_name = serializers.ReadOnlyField(source='building.name')
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'building', 'building_name', 'unit_type', 'status', 'number', 'area', 'monthly_rent', 'image_url', 'created_at', 'updated_at')

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ('id', 'full_name', 'phone_number', 'email', 'created_at', 'updated_at')

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    unit_number = serializers.ReadOnlyField(source='unit.number')
    class Meta:
        model = MaintenanceRequest
        fields = ('id', 'unit', 'unit_number', 'description', 'request_date', 'is_resolved', 'resolved_date')

class ExpenseSerializer(serializers.ModelSerializer):
    building_name = serializers.ReadOnlyField(source='building.name')
    class Meta:
        model = Expense
        fields = ('id', 'building', 'building_name', 'description', 'amount', 'date')

class TenantBankAccountSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.full_name')
    class Meta:
        model = TenantBankAccount
        fields = ('id', 'tenant', 'tenant_name', 'bank_name', 'account_number', 'iban')

class RentReportSerializer(serializers.ModelSerializer):
    building_name = serializers.ReadOnlyField(source='building.name')
    class Meta:
        model = RentReport
        fields = ('id', 'building', 'building_name', 'total_income', 'generated_date')