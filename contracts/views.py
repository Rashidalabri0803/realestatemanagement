from django.shortcuts import render, get_object_or_404, redirect
from .models import Contract
from .forms import ContractForm

def contract_list(request):
    contracts = Contract.objects.all()
    return render(request, 'contracts/contract_list.html', {'contracts': contracts})

def contract_detail(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    return render(request, 'contracts/contract_detail.html', {'contract': contract})

def contract_create(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contract_list')
    else:
        form = ContractForm()
    return render(request, 'contracts/contract_create.html', {'form': form})