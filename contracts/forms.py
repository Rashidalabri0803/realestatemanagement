from django import forms
from .models import Contract

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['property', 'tenant_name', 'start_date', 'end_date', 'terms']