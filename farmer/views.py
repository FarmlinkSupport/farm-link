from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from accounts.models import User
from rest_framework import permissions
from accounts.renderers import UserRenderer
from rest_framework.response import Response
from accounts.serializers import UserProfileSerializer
from .models import Farmer
from contract.models import Contract,ContractDeployment
from rest_framework.generics import RetrieveAPIView
from contract.serializers import ContractDeliveryGet

class FarmerProfileView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    renderer_classes=[UserRenderer]

    def post(self,request,*args,**kwargs):
        serializer=FarmerProfileRegSerializer(data=request.data,context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({'message':'farmer successfully registered!!'},status=status.HTTP_201_CREATED)
    
    def get(self,request,*args,**kwargs):
        farmer_profile = Farmer.objects.get(user=request.user)
        serializer = FarmerProfileViewSerilaizer(farmer_profile)
        user = UserProfileSerializer(request.user)
        return Response({'data': [user.data,serializer.data]},status=status.HTTP_200_OK)

class FarmerProfileDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get(self,request,user_id,*args,**kwargs):
        user = User.objects.get(id=user_id)
        if user is None:
            return Response('User not found',status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user)
        profile = Farmer.objects.get(user=user)
        profile_serializer = FarmerProfileViewSerilaizer(profile)
        if profile_serializer.data is None:
            profile_serializer.data =[]
        return Response([serializer.data,profile_serializer.data],status=status.HTTP_200_OK)

class FarmerContractView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get(self, request, *args, **kwargs):
        try:
            # Get all contracts where the user is the farmer
            contracts = Contract.objects.filter(farmer=request.user)
            contract_farmer = []
            
            for contract in contracts:
                deploy = ContractDeployment.objects.filter(contract=contract).first()
                
                if deploy and not deploy.farmeragreed and not deploy.deploy_status:
                    contract_farmer.append(contract)
            
            if not contract_farmer:
                return Response({'message': 'No contracts found'}, status=status.HTTP_204_NO_CONTENT)
            
            serializers = ContractDeliveryGet(contract_farmer, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Catch any unexpected errors and return a 500 error with the exception message
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
