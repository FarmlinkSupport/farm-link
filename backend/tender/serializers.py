from rest_framework import serializers
from .models import Tender

class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = ['id','title','open_time','close_time','status','minimum_bid','maximum_bid','description','notice_file']

    def create(self, validated_data):
        user=validated_data.pop('company_id')
        return Tender.objects.create(company_id=user,**validated_data)

        
