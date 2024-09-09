from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from accounts.models import User
from rest_framework import permissions
from accounts.renderers import UserRenderer
from rest_framework.response import Response
from accounts.serializers import UserProfileSerializer
from .models import Farmer
from rest_framework.generics import RetrieveAPIView

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
