from rest_framework import serializers
from .models import Contract,ContractDeliveryStatus

class ContractSerilaizer(serializers.ModelSerializer):
    farmer_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = ['id', 'title', 'farmer_name', 'buyer_name', 'status', 'payment_status']

    def get_farmer_name(self,obj):
        return obj.farmer.name
    
    def get_buyer_name(self,obj):
        return obj.buyer.name
    
    def get_title(self,obj):
        return obj.tender.title

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
        model = Contract
        fields = ['id', 'farmer', 'buyer', 'start_date', 'end_date', 'status']

        