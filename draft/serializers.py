from rest_framework import serializers
from .models import Draft
from .models import Tender
from accounts.models import User

class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ['draftfile']

    def create(self, validated_data):
        tender_id=validated_data.pop('tender_id')
        tender=Tender.objects.get(id=tender_id)
        if tender is None:
            return serializers.ValidationError('Tender id is incorrect please check !!')
        user = validated_data.pop('user')
        farmer=User.objects.get(id=user)
        return Draft.objects.create(farmer=farmer,tender=tender,**validated_data)
    
class DraftGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = '__all__'

class DraftUpdateBuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ['status']