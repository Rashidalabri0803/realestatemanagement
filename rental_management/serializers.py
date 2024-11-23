from rest_framework import serializers

from .models import Building, Units, Invoice, LeaseContract, Tenant


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

class UnitsSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source='building.name', read_only=True)
    
    class Meta:
        model = Units
        fields = ['id', 'building', 'building_name', 'unit_type', 'number', 'area', 'monthly_rent', 'is_available']

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'

class LeaseContractSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.full_name', read_only=True)
    unit_number = serializers.CharField(source='unit.number', read_only=True)
    
    class Meta:
        model = LeaseContract
        fields = ['id', 'tenant', 'tenant_name', 'unit', 'unit_number', 'start_date', 'end_date', 'total_amount', 'is_active', 'document']

class InvoiceSerializer(serializers.ModelSerializer):
    contract_info = LeaseContractSerializer(source='contract.__str__', read_only=True)
    class Meta:
        model = Invoice
        fields = ['id', 'contract', 'contract_info', 'amount_due', 'due_date', 'is_paid', 'payment_date']