from django.shortcuts import render
from rest_framework import status,permissions
from rest_framework.response import Response
from .models import Contract,ContractDeliveryStatus,ContractDeployment
from rest_framework.views import APIView
from .serializers import ContractDeliverySerializer,ContractDeliverySerializerStatus,ContractDeliveryGet,ContractSerilaizer
from accounts.renderers import UserRenderer
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from payment.models import Payment
import stripe

class ContractDeliveryStatusView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    renderer_classes=[UserRenderer]

    def post(self,request,id,*args,**kwargs):
        try:
            contract=Contract.objects.get(id=id)
            pay=Payment.objects.get(contract=contract)
            deploy = ContractDeployment.objects.filter(contract=contract).first()
            if deploy is None:
                return Response('Contract has not been deployed yet!',status=status.HTTP_404_NOT_FOUND)
            if deploy.deploy_status == False:
                return Response('Contract isn\'t deployed yet',status=status.HTTP_400_BAD_REQUEST)
            if request.user != contract.farmer:
                return PermissionDenied('You are not authorized to this page!')
            serializer=ContractDeliverySerializer(data=request.data)
            serializer.save(contract_id = id)
            return Response({'message':'Contract Delivery Status has been Addded'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Payment has not been yet for the contract id : {id}',status=status.HTTP_402_PAYMENT_REQUIRED)
    
    def put(self,request,id,*args,**kwargs):
        try:
            contract=Contract.objects.get(id=id)
            pay=Payment.objects.get(contract=contract)
            if contract is None:
                return Response({'msg':"Contract doesn't exists!!"},status=status.HTTP_404_NOT_FOUND)
            if request.user != contract.buyer:
                return PermissionDenied('You are not authorized to this page!')
            delivery=ContractDeliveryStatus.objects.filter(contract=contract).first()
            if delivery is None:
                return Response({'msg':"Contract delivery data doesn't exists!!"},status=status.HTTP_404_NOT_FOUND)
            serializer=ContractDeliverySerializerStatus(delivery,data=request.data)
            serializer.save()
            if serializer.data['buyer_status'] == "Completed" and contract.status != "Completed":
                pay=Payment.objects.get(contract=contract)
                payment_intent=stripe.PaymentIntent.retrieve(pay.payment_intent)
                transfer = stripe.Transfer.create(
                    amount=payment_intent.amount_received,  
                    currency=payment_intent.currency,       
                    destination="acct_1PxU5xP0UyL2PaGn",                
                    transfer_group=payment_intent.transfer_group 
                )
                contract.payment_status="Completed"
                contract.status="Completed"
                contract.save()

            return Response({'message':'Contract Delivery Status has been changed successfully!'},status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(f'Payment has not been yet for the contract id : {id}',status=status.HTTP_402_PAYMENT_REQUIRED)
        
    def get(self,request,id,*args,**kwargs):
        try:
            if request.path !="/favicon.ico":
                contract=Contract.objects.get(id=id)
                if contract is None:
                    return Response({'msg':"Contract doesn't exists!!"},status=status.HTTP_404_NOT_FOUND)
                if request.user == contract.farmer or request.user == contract.buyer:
                    delivery = ContractDeliveryStatus.objects.filter(contract=contract).first()
                    if delivery is None:
                        return Response({'msg':"Contract delivery data doesn't exists!!"},status=status.HTTP_404_NOT_FOUND)
                    serializer=ContractDeliveryGet(delivery)
                    return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response("User is not authorized to get the data",status=status.HTTP_401_UNAUTHORIZED)


class ContractGetView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    renderer_classes=[UserRenderer]
    
    def get(self,request,*args,**kwargs):
        try:
            if request.path != "/favicon.ico":
                contract=Contract.objects.filter(Q(buyer=request.user) | Q(farmer=request.user))
                if contract is None:
                    return Response("User doesn't have any Contract!",status=status.HTTP_204_NO_CONTENT)
                serializer=ContractSerilaizer(contract,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response('User has no contract !!',status=status.HTTP_204_NO_CONTENT)

class ContractDeclineView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,id,*args,**kwargs):
        contract=Contract.objects.get(id=id)
        if contract is not None:
            contract.status="Terminated"
            contract.save()
            return Response('Contract has been declined successfully',status=status.HTTP_202_ACCEPTED)
