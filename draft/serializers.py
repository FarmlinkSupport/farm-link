from rest_framework import serializers
from .models import Draft
from .models import Tender

class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ['draftfile']

    def create(self, validated_data):
        tender_id=validated_data.pop('tender_id')
        tender=Tender.objects.get(id=tender_id)
        if tender is None:
            return serializers.ValidationError('Tender id is incorrect please check !!')
        farmer=validated_data.pop('user')
        return Draft.objects.create(farmer=farmer,tender=tender,**validated_data)
    
class DraftGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = '__all__'

class DraftUpdateBuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ['status']