from django import forms

from .models import (
    Building,
    Unit,
    Tenant,
    LeaseContract,
    Payment,
    MaintenanceRequest,
    Expense,
    Notifiction,
    Attachment
)


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'address', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placholder': 'اسم المبنى'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placholder': 'عنوان المبنى'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placholder': 'وصف المبنى'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Building.objects.filter(name=name).exists():
            raise forms.ValidationError('اسم المبنى موجود بالفعل يرجي اختيار اسم اخر.')
        return name

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['building', 'unit_type', 'status', 'number', 'area', 'monthly_rent', 'image']
        widgets = {
            'building': forms.Select(attrs={'class': 'form-control'}),
            'unit_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placholder': 'رقم الوحدة'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'placholder': 'المساحة'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placholder': 'الإجمالي الشهري'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_area(self):
        area = self.cleaned_data.get('area')
        if area < 10:
            raise forms.ValidationError('مساحة الوحدة يجب أن تكون أكبر من 10 متر مربع.')
        return area

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['full_name', 'phone_number', 'email', 'id_card', 'profile_picture', 'description']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placholder': 'الاسم المستأجر'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placholder': 'رقم الهاتف'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placholder': 'البريد الإلكتروني'}),
            'id_card': forms.TextInput(attrs={'class': 'form-control', 'placholder': 'رقم الهوية'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placholder': 'ملاحظات إضافية'})
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError('رقم الهاتف يجب أن يحتوي على أرقام فقط.')
        return phone_number

class LeaseContractForm(forms.ModelForm):
    class Meta:
        model = LeaseContract
        fields = ['unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'is_active']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placholder': 'الإيجار الشهري'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date <= start_date:
            raise forms.ValidationError('تاريخ نهاية العقد يجب أن يكون أكبر من تاريخ البدء.')
        return end_date

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['contract', 'amount', 'payment_date', 'description']
        widgets = {
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placholder': 'المبلغ'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placholder': 'وصف الدفع'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('المبلغ يجب أن يكون أكبر من صفر.')
        return amount
        
class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['unit', 'description', 'request_date', 'is_resolved', 'resolved_date']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placholder': 'وصف المشكلة'}),
            'request_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_resolved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'resolved_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    def clean_resolved_date(self):
        request_date = self.cleaned_data.get('request_date')
        resolved_date = self.cleaned_data.get('resolved_date')
        if resolved_date and request_date < resolved_date:
            raise forms.ValidationError('تاريخ المعالجة يجب أن يكون أكبر من تاريخ الطلب.')
        return resolved_date

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['building', 'description', 'amount', 'date']
        widgets = {
            'building': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placholder': 'وصف المصروف'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placholder': 'المبلغ'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('المبلغ يجب أن يكون أكبر من صفر.')
        return amount

class NotifictionForm(forms.ModelForm):
    class Meta:
        model = Notifiction
        fields = ['message', 'is_read']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placholder': 'نص الإشعار'}),
            'is_read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['contract', 'file', 'description']
        widgets = {
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placholder': 'وصف الملف'})
        }