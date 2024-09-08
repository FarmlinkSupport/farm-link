from django.shortcuts import render
from rest_framework import status,permissions
from rest_framework.response import Response
from .models import Contract,ContractDeliveryStatus,ContractDeployment
from rest_framework.views import APIView
from .serializers import ContractDeliverySerializer,ContractDeliverySerializerStatus,ContractDeliveryGet
from accounts.renderers import UserRenderer
from django.core.exceptions import PermissionDenied


class ContractDeliveryStatusView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    renderer_classes=[UserRenderer]

    def post(self,request,id,*args,**kwargs):
        contract=Contract.objects.get(id=id)
        deploy = ContractDeployment.objects.get(contract=contract)
        if deploy.deploy_status == False:
            return Response('Contract isn\'t deployed yet',status=status.HTTP_400_BAD_REQUEST)
        if contract is None:
            return Response({'msg':"Contract doesn't exists!!"},status=status.HTTP_404_NOT_FOUND)
        if request.user != contract.farmer:
            return PermissionDenied('You are not authorized to this page!')
        serializer=ContractDeliverySerializer(data=request.data)
        serializer.save(contract_id = id)
        return Response({'message':'Contract Delivery Status has been Addded'},status=status.HTTP_200_OK)
    
    def put(self,request,id,*args,**kwargs):
        contract=Contract.objects.get(id=id)
        if contract is None:
            return Response({'msg':"Contract doesn't exists!!"},status=status.HTTP_404_NOT_FOUND)
        if request.user != contract.buyer:
            return PermissionDenied('You are not authorized to this page!')
        delivery=ContractDeliveryStatus.objects.get(contract=contract)
        if delivery is None:
            return Response({'msg':"Contract delivery data doesn't exists!!"},status=status.HTTP_404_NOT_FOUND)
        serializer=ContractDeliverySerializerStatus(delivery,data=request.data)
        serializer.save()
        return Response({'message':'Contract Delivery Status has been changed successfully!'},status=status.HTTP_202_ACCEPTED)
    
    def get(self,request,id,*args,**kwargs):
        contract=Contract.objects.get(id=id)
        if contract is None:
            return Response({'msg':"Contract doesn't exists!!"},status=status.HTTP_404_NOT_FOUND)
        if request.user == contract.farmer or request.user == contract.buyer:
            delivery = ContractDeliveryStatus.objects.get(contract=contract)
            if delivery is None:
                return Response({'msg':"Contract delivery data doesn't exists!!"},status=status.HTTP_404_NOT_FOUND)
            ContractDeliveryGet(delivery)
            return Response(ContractDeliveryGet.data,status=status.HTTP_200_OK)
        return Response("User is not authorized to get the data",status=status.HTTP_401_UNAUTHORIZED)

