from django.shortcuts import render, get_object_or_404, redirect
from .models import Invoice
from .forms import InvoiceForm

def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})