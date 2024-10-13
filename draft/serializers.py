from rest_framework import serializers
from .models import Draft, Tender
from accounts.models import User

class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ['draftfile']

    def create(self, validated_data):
        tender_id = validated_data.pop('tender_id', None)
        user_id = validated_data.pop('user', None)

        try:
            tender = Tender.objects.get(id=tender_id)
        except Tender.DoesNotExist:
            raise serializers.ValidationError('Tender id is incorrect, please check!')

        try:
            farmer = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist!')

        # Save the draft with the file, tender, and farmer
        draft = Draft.objects.create(farmer=farmer, tender=tender, **validated_data)
        return draft
    
class DraftGetSerializer(serializers.ModelSerializer):
    tender_title = serializers.SerializerMethodField()
    farmer_name = serializers.SerializerMethodField()

    class Meta:
        model = Draft
        fields = ['id','farmer','farmer_name','tender','tender_title','status','draftfile','timestamp']

    def get_tender_title(self,obj):
        return obj.tender.title
    
    def get_farmer_name(self,obj):
        return obj.farmer.name

class DraftUpdateBuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ['status']