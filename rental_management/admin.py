from django.contrib import admin
from .models import Building, Units, Tenant, LeaseContract

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name',)

@admin.register(Units)
class UnitsAdmin(admin.ModelAdmin):
    list_display = ('building', 'unit_type', 'number', 'monthly_rent')
    list_filter = ('unit_type',)
    search_fields = ('number',)

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email')
    search_fields = ('full_name', 'phone_number',)

@admin.register(LeaseContract)
class LeaseContractAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'unit', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')