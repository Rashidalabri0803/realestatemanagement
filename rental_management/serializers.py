from rest_framework import serializers

from .models import (
    Building,
    Unit,
    Tenant,
    LeaseContract,
    Payment,
    MaintenanceRequest,
    Expense,
    Notifiction,
)


class BuildingSerializer(serializers.ModelSerializer):
    total_units = serializers.SerializerMethodField()
    total_rent = serializers.SerializerMethodField()
    yearly_rent = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Building
        fields = ('id', 'name', 'address', 'description', 'image_url', 'total_units', 'total_rent', 'yearly_rent', 'created_at', 'updated_at')

    def get_total_units(self, obj):
        return obj.unit_set.count()

    def get_total_rent(self, obj):
        return obj.total_rent()

    def get_yearly_rent(self, obj):
        return obj.yearly_rent()

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class UnitSerializer(serializers.ModelSerializer):
    building_name = serializers.ReadOnlyField(source='building.name')
    tenant_name = serializers.SerializerMethodField()
    yearly_rent = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'building', 'building_name', 'unit_type', 'status', 'number', 'area', 'monthly_rent', 'yearly_rent', 'tenant_name', 'image_url', 'created_at', 'updated_at')

    def get_tenant_name(self, obj):
        contract = LeaseContract.objects.filter(unit=obj, is_active=True).first()
        if contract:
            return contract.tenant.full_name
        return 'غير مؤجرة'

    def get_yearly_rent(self, obj):
        return obj.building.yearly_rent()

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class TenantSerializer(serializers.ModelSerializer):
    active_contracts = serializers.SerializerMethodField()
    
    class Meta:
        model = Tenant
        fields = ('id', 'full_name', 'phone_number', 'email', 'id_card', 'profile_picture', 'description', 'active_contracts')

    def get_active_contracts(self, obj):
        return LeaseContract.objects.filter(tenant=obj, is_active=True).count()

class LeaseContractSerializer(serializers.ModelSerializer):
    unit_details = UnitSerializer(source='unit', read_only=True)
    tenant_detaile = TenantSerializer(source='tenant', read_only=True)
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = LeaseContract
        fields = ('id', 'unit', 'unit_details', 'tenant', 'tenant_details', 'start_date', 'end_date', 'monthly_rent', 'is_active', 'remaining_days')

    def get_remaining_days(self, obj):
        return obj.remaining_days()

    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError('تاريخ الانتهاء يجب أن يكون أكبر من تاريخ البدء.')
        return data

class PaymentSerializer(serializers.ModelSerializer):
    contract_details = LeaseContractSerializer(source='contract', read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'contract', 'contract_details', 'amount', 'payment_date', 'description')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('المبلغ يجب أن يكون أكبر من صفر.')
        return value
        
class MaintenanceRequestSerializer(serializers.ModelSerializer):
    unit_details = UnitSerializer(source='unit', read_only=True)
    class Meta:
        model = MaintenanceRequest
        fields = ('id', 'unit', 'unit_details', 'description', 'request_date', 'is_resolved', 'resolved_date')

    def validate_resolved_date(self, value):
        request_date = self.validated_data.get('request_date')
        if value and request_date and value < request_date:
            raise serializers.ValidationError('تاريخ المعالجة يجب أن يكون أكبر من تاريخ الطلب.')
        return value

class ExpenseSerializer(serializers.ModelSerializer):
    building_name = serializers.ReadOnlyField(source='building.name')
    class Meta:
        model = Expense
        fields = ('id', 'building', 'building_name', 'description', 'amount', 'date')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('المبلغ يجب أن يكون أكبر من صفر.')
        return value

class NotifictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifiction
        fields = ('id', 'message', 'created_at', 'is_read')