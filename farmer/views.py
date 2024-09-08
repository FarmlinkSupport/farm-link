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
    serializer_class = FarmerProfileViewSerilaizer
    lookup_field = 'user__id'

    def get_queryset(self):
        return Farmer.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        farmer_profile = self.get_queryset().first()
        serializer = self.get_serializer(farmer_profile)
        user_serializer = UserProfileSerializer(request.user)
        return Response({'user': user_serializer.data, 'profile': serializer.data}, status=status.HTTP_200_OK)
