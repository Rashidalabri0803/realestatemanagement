from django.contrib import admin
from .models import Contract

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant_name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('tenant_name', 'property__name')