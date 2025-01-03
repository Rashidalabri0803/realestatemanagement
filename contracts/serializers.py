from rest_framework import serializers
from .models import LeasContract

class LeasContractSerialiser(serializers.ModelSerializer):
    class Meta:
        model = LeasContract
        fields = '__all__'