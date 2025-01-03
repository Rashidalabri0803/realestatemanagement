from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'propert_type', 'owner']
    list_filter = ['propert_type']
    search_fields = ['name', 'address']