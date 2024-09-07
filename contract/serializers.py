from rest_framework import serializers
from .models import Contract,ContractDeliveryStatus

class ContractSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
    

class ContractDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractDeliveryStatus
        fields = ['contract','invoice_file']

    def create(self, validated_data):
        id=validated_data.pop('contract_id')
        contract=Contract.objects.get(id=id)
        return ContractDeliveryStatus.objects.create(contrcat=contract,**validated_data)
    
class ContractDeliverySerializerStatus(serializers.ModelSerializer):
    class Meta:
        model = ContractDeliveryStatus
        fields = ['status']

class ContractDeliveryGet(serializers.ModelSerializer):
    class Meta:
        model = ContractDeliveryStatus
        fields = "__all__"
        