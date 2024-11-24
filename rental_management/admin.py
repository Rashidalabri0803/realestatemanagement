from django.contrib import admin

from .models import Building, LeaseContract, Tenant


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created_at', 'updated_at', 'image_preview')
    search_fields = ('name', 'address')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return f"<img src='{obj.image.url}' width='50' height='50'/>"
        return "لا توجد صورة"
    image_preview.allow_tags = True
    image_preview.short_description = 'صورة المبني'
    



@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email')
    search_fields = ('full_name', 'phone_number', 'email')

@admin.register(LeaseContract)
class LeaseContractAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'unit', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')