from rest_framework import serializers

from .models import (
    Building,
    Expense,
    LeaseContract,
    MaintenanceRequest,
    Notifiction,
    Payment,
    Tenant,
    Unit,
)


class BuildingSerializer(serializers.ModelSerializer):
    total_units = serializers.SerializerMethodField()
    total_income = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Building
        fields = ('id', 'name', 'address', 'descriptin', 'image_url', 'total_units', 'total_income', 'created_at', 'updated_at')

    def get_total_units(self, obj):
        return obj.unit_set.count()

    def get_total_income(self, obj):
        contracts = LeaseContract.objects.filter(unit__building=obj)
        return sum(contract.monthly_rent for contract in contracts)

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class UnitSerializer(serializers.ModelSerializer):
    building_name = serializers.ReadOnlyField(source='building.name')
    tenant_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'building', 'building_name', 'unit_type', 'status', 'number', 'area', 'monthly_rent', 'tenant_name', 'image_url', 'created_at', 'updated_at')

    def get_tenant_name(self, obj):
        contract = LeaseContract.objects.filter(unit=obj, is_active=True).first()
        if contract:
            return contract.tenant.full_name
        return 'غير مؤجرة'

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class TenantSerializer(serializers.ModelSerializer):
    active_contracts = serializers.SerializerMethodField()
    
    class Meta:
        model = Tenant
        fields = ('id', 'full_name', 'phone_number', 'email', 'description', 'active_contracts')

    def get_active_contracts(self, obj):
        return LeaseContract.objects.filter(tenant=obj, is_active=True).count()

class LeaseContractSerializer(serializers.ModelSerializer):
    unit_details = UnitSerializer(source='unit', read_only=True)
    tenant_name = serializers.ReadOnlyField(source='tenant.full_name')
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = LeaseContract
        fields = ('id', 'unit', 'unit_details', 'tenant_name', 'start_date', 'end_date', 'monthly_rent', 'is_active', 'remaining_days')

    def get_remaining_days(self, obj):
        return obj.remaining_days()

class PaymentSerializer(serializers.ModelSerializer):
    contract_details = LeaseContractSerializer(source='contract', read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'contract', 'contract_details', 'amount', 'payment_date', 'description')
        
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

class NotifictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifiction
        fields = ('id', 'message', 'created_at', 'is_read')