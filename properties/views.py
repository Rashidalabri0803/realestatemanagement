from django.shortcuts import render, redirect

from .models import Property

from .forms import PropertyForm

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})