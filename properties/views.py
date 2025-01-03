from django.shortcuts import redirect, render

from .forms import PropertyForm
from .models import Property


def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})

def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('property_list')
    else:
        form = PropertyForm()
    return render(request, 'properties/property_create.html', {'form': form})