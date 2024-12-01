from django import forms
from .models import Unit, LeaseContract, MaintenanceRequest, Reminder

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['building', 'unit_type', 'status', 'number', 'area', 'monthly_rent']
        widgets = {
            'building': forms.Select(attrs={'class': 'form-control'}),
            'unit_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الوحدة'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المساحة'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'الإيجار الشهري'}),
        }

    def clean_monthly_rent(self):
        monthly_rent = self.cleaned_data.get('monthly_rent')
        if monthly_rent <= 0:
            raise forms.ValidationError("الإيجار الشهري يجب أن يكون أكبر من الصفر")
        return monthly_rent

class LeaseContractForm(forms.ModelForm):
    class Meta:
        model = LeaseContract
        fields = ['tenant', 'unit', 'start_date', 'end_date', 'monthly_rent', 'is_active']
        widgets = {
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'تاريخ البدء'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'تاريخ الانتهاء'})
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("تاريخ البدء يجب أن يكون قبل تاريخ الانتهاء")
        return cleaned_data

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['unit', 'description', 'priority']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'وصف المشكلة'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 100:
            raise forms.ValidationError("الوصف يجب أن يكون أكثر تفصيلاً")
        return description

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['tenant', 'contract', 'message']
        widgets = {
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رسالة التنبيه'})
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 5:
            raise forms.ValidationError("رسالة التذكير يجب أن تكون أكثر تفصيلا")
        return message