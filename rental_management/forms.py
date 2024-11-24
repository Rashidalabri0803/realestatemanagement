from django import forms
from .models import Building, Unit, Tenant, MaintenanceRequest, Expense, TenantBankAccount, RentReport, LeaseContract

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'address', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['building', 'unit_type', 'status', 'number', 'area', 'monthly_rent', 'image']
        widgets = {
            'building': forms.Select(attrs={'class': 'form-control'}),
            'unit_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['full_name', 'phone_number', 'email', 'description']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['unit', 'description', 'request_date', 'is_resolved', 'resolved_date']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'request_date': forms.DateInput(attrs={'class': 'form-control'}),
            'is_resolved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'resolved_date': forms.DateInput(attrs={'class': 'form-control'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['building', 'description', 'amount', 'date']
        widgets = {
            'building': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
        }

class TenantBankAccountForm(forms.ModelForm):
    class Meta:
        model = TenantBankAccount
        fields = ['tenant', 'bank_name', 'account_number', 'iban']
        widgets = {
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'iban': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RentReportForm(forms.ModelForm):
    class Meta:
        model = RentReport
        fields = ['building', 'total_income']
        widgets = {
            'building': forms.Select(attrs={'class': 'form-control'}),
            'total_income': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def clean_total_income(self):
        total_income = self.cleaned_data.get('total_income')
        if total_income <= 0:
            raise forms.ValidationError('إجمالي الدخل يجب أن يكون أكبر من الصفر')
        return total_income