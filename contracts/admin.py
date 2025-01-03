from django.contrib import admin
from .models import LeasContract

@admin.register(LeasContract)
class LeasContractAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'property', 'start_date', 'end_date', 'monthly_rent', 'is_active']
    list_filter = ['is_active', 'start_date']
    search_fields = ['tenant__name', 'property__name']