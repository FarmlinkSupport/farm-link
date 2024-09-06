from rest_framework import serializers
from .models import Farmer

class FarmerProfileRegSerializer(serializers.ModelSerializer):
    class Meta:
        model=Farmer
        fields = ['farm_name', 'farm_location', 'farm_size']
    
    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['user']=user
        return Farmer.objects.create(**validated_data)

class FarmerProfileViewSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['farm_name', 'farm_location', 'farm_size']