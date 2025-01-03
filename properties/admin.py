from django.contrib import admin

from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'occupied')
    list_filter = ('type', 'occupied')
    search_fields = ('name',)