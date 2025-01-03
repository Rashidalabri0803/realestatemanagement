from django.shortcuts import render
from .models import Property
from .serialisers import PropertySerialiser
from rest_framework import viewsets

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerialiser