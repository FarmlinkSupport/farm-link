from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from accounts.renderers import UserRenderer
from .serializers import BuyerProfileSerializer
from accounts.serializers import UserProfileSerializer
from .models import Profile
from accounts.models import User
from rest_framework.generics import RetrieveAPIView
from contract.models import Contract,ContractDeployment
from contract.serializers import ContractDeliveryGet

class BuyerProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = BuyerProfileSerializer(data=request.data, context={'user': request.user, 'verify': True})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Buyer profile created!"}, status=status.HTTP_201_CREATED)
    
    def get(self, request, *args, **kwargs):
        if request.path != "favicon.ico":
            buyer_profile = Profile.objects.get(user=request.user)
            serializer = BuyerProfileSerializer(buyer_profile)
            user_serializer = UserProfileSerializer(request.user)
            return Response({'user': user_serializer.data, 'profile': serializer.data}, status=status.HTTP_200_OK)
        return Response('Buyer has no profile',status=status.HTTP_204_NO_CONTENT)

class BuyerProfileDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]
    
    def get(self,request,user_id,*args,**kwargs):
        user = User.objects.get(id=user_id)
        if user is None:
            return Response('User not found',status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user)
        profile = Profile.objects.get(user=user)
        profile_serializer = BuyerProfileSerializer(profile)
        if profile_serializer.data is None:
            profile_serializer.data =[]
        return Response([serializer.data,profile_serializer.data],status=status.HTTP_200_OK)

class BuyerContractView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        contractdep=Contract.objects.filter(buyer=request.user)
        contract_buyer=[]
        for con in contractdep:
            contract=ContractDeployment.objects.get(contract=con)
            if not contract.deploy_status and contract.farmeragreed==True:
                contract_buyer.append(con)
        serializer=ContractDeliveryGet(contract_buyer,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        