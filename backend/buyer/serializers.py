from rest_framework import serializers
from .models import Profile

class BuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['company_name','company_address','company_zipcode','gst_no']
    
    def create(self, validated_data):
        user=self.context.get('user')
        validated_data['user']=user
        is_verified=self.context.get('verify')
        validated_data['is_verified']=is_verified
        return Profile.objects.create(**validated_data)