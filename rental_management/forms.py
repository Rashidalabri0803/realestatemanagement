from django import forms
from .models import Building, Unit, Tenant, LeaseContract, Invoice, Payment, Reminder, MaintenanceRequest, MaintenanceFeedback, LatePayment, Notification, Report, SystemSettings

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ('name', 'address', 'description', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المبنى'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان المبنى'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'وصف المبنى'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        
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

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ('full_name', 'phone_number', 'email', 'id_card', 'profile_picture')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الكامل'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
            'id_card': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الرقم الهوية'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class LeaseContractForm(forms.ModelForm):
    class Meta:
        model = LeaseContract
        fields = ['unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'is_active']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type' : 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type' : 'date'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'الإيجار الشهري'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("تاريخ البدء يجب أن يكون قبل تاريخ الانتهاء")
        return cleaned_data

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['contract', 'issue_date', 'due_date', 'amount', 'is_paid', 'late_fee']
        widgets = {
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type' : 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type' : 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المبلغ'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'late_fee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'غرامة التأخير'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['contract', 'amount', 'payment_date', 'description']
        widgets = {
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المبلغ المدفوع'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type' : 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'وصف الدفع'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("المبلغ يجب أن يكون أكبر من الصفر")
        return amount

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['tenant', 'contract', 'message']
        widgets = {
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'رسالة التذكير'})
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("رسالة التذكير يجب أن تكون أكثر تفصيلا")
        return message

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

class MaintenanceFeedbackForm(forms.ModelForm):
    class Meta:
        model = MaintenanceFeedback
        fields = ['maintenance_requests', 'rating', 'comments']
        widgets = {
            'maintenance_requests': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'التقييم (من ١ إلى ٥)'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'تعليقاتك'})
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not ( 1 <= rating <= 5):
            raise forms.ValidationError("التقييم يجب أن يكون بين 1 و 5")
        return rating

class LatePaymentForm(forms.ModelForm):
    class Meta:
        model = LatePayment
        fields = ['invoice', 'days_late', 'penalty']
        widgets = {
            'invoice': forms.Select(attrs={'class': 'form-control'}),
            'days_late': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'عدد الأيام المتأخرة'}),
            'penalty': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'غرامة التأخير'}),
        }

    def clean_days_late(self):
        days_late = self.cleaned_data.get('days_late')
        if days_late < 0:
            raise forms.ValidationError("عدد الأيام المتأخرة لا يمكن أن يكون سالبا")
        return days_late

    def clean_penalty(self):
        penalty = self.cleaned_data.get('penalty')
        if penalty < 0:
            raise forms.ValidationError("غرامة التأخير لا يمكن أن تكون سالبا")
        return penalty

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message', 'is_read', 'priority']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'نص الرسالة'}),
            'is_read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("الرسالة يجب أن تحتوي على ١٠ أحرف على الأقل")
        return message

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'report_type', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم التقرير'}),
            'report_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نوع التقرير'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'محتوى التقرير'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 5:
            raise forms.ValidationError("اسم التقرير يجب أن يكون أقل من 5 حرف")
        return name

class SystemSettingsForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = ['key', 'value', 'description']
        widgets = {
            'key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم الإعداد'}),
            'value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'القيمة'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'الوصف'}),
        }

    def clean_key(self):
        key = self.cleaned_data.get('key')
        if len(key) < 3:
            raise forms.ValidationError("اسم الإعداد يجب أن يحتوى على  3 حرف على أقل")
        return key