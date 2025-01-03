from django.shortcuts import render
from .models import Tenant
from .serialisers import TenantSerialiser
from rest_framework import viewsets

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerialiser