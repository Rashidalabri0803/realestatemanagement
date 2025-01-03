from rest_framework import viewsets
from .models import LeasContract
from .serialisers import LeasContractSerialiser

class LeasContractViewSet(viewsets.ModelViewSet):
    queryset = LeasContract.objects.all()
    serializer_class = LeasContractSerialiser