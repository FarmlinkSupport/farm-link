from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from asgiref.sync import sync_to_async
from .models import Contract, ContractDeliveryStatus, ContractDeployment
from .serializers import ContractDeliverySerializer, ContractDeliverySerializerStatus, ContractDeliveryGet
from accounts.renderers import UserRenderer
from django.core.exceptions import PermissionDenied

class ContractDeliveryStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    async def post(self, request, id, *args, **kwargs):
        contract = await sync_to_async(Contract.objects.get)(id=id)
        deploy = await sync_to_async(ContractDeployment.objects.get)(contract=contract)
        if not deploy.deploy_status:
            return Response('Contract isn\'t deployed yet', status=status.HTTP_400_BAD_REQUEST)
        if not contract:
            return Response({'msg': "Contract doesn't exist!!"}, status=status.HTTP_404_NOT_FOUND)
        if request.user != contract.farmer:
            raise PermissionDenied('You are not authorized to this page!')
        serializer = ContractDeliverySerializer(data=request.data)
        if serializer.is_valid():
            await sync_to_async(serializer.save)(contract_id=id)
            return Response({'message': 'Contract Delivery Status has been Added'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    async def put(self, request, id, *args, **kwargs):
        contract = await sync_to_async(Contract.objects.get)(id=id)
        if not contract:
            return Response({'msg': "Contract doesn't exist!!"}, status=status.HTTP_404_NOT_FOUND)
        if request.user != contract.buyer:
            raise PermissionDenied('You are not authorized to this page!')
        delivery = await sync_to_async(ContractDeliveryStatus.objects.get)(contract=contract)
        if not delivery:
            return Response({'msg': "Contract delivery data doesn't exist!!"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContractDeliverySerializerStatus(delivery, data=request.data)
        if serializer.is_valid():
            await sync_to_async(serializer.save)()
            return Response({'message': 'Contract Delivery Status has been changed successfully!'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    async def get(self, request, id, *args, **kwargs):
        contract = await sync_to_async(Contract.objects.get)(id=id)
        if not contract:
            return Response({'msg': "Contract doesn't exist!!"}, status=status.HTTP_404_NOT_FOUND)
        if request.user != contract.farmer and request.user != contract.buyer:
            return Response("User is not authorized to get the data", status=status.HTTP_401_UNAUTHORIZED)
        delivery = await sync_to_async(ContractDeliveryStatus.objects.get)(contract=contract)
        if not delivery:
            return Response({'msg': "Contract delivery data doesn't exist!!"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContractDeliveryGet(delivery)
        return Response(serializer.data, status=status.HTTP_200_OK)
