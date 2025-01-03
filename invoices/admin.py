from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('contract', 'issue_date', 'due_date', 'amount', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('contract__tenant_name',)