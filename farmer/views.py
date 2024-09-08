from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from asgiref.sync import sync_to_async
from .serializers import FarmerProfileRegSerializer, FarmerProfileViewSerilaizer
from accounts.models import User
from accounts.renderers import UserRenderer
from accounts.serializers import UserProfileSerializer
from .models import Farmer

class FarmerProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    async def post(self, request, *args, **kwargs):
        serializer = FarmerProfileRegSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        user = await sync_to_async(serializer.save)()
        return Response({'message': 'Farmer successfully registered!'}, status=status.HTTP_201_CREATED)
    
    async def get(self, request, *args, **kwargs):
        farmer_profile = await sync_to_async(Farmer.objects.get)(user=request.user)
        serializer = FarmerProfileViewSerilaizer(farmer_profile)
        user_serializer = UserProfileSerializer(request.user)
        return Response({'data': [user_serializer.data, serializer.data]}, status=status.HTTP_200_OK)

class FarmerProfileDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = FarmerProfileViewSerilaizer
    lookup_field = 'user__id'

    async def get_queryset(self):
        return await sync_to_async(Farmer.objects.filter)(user=self.request.user)

    async def get(self, request, *args, **kwargs):
        farmer_profile = (await self.get_queryset()).first()
        if farmer_profile is None:
            return Response({'error': 'Farmer profile not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(farmer_profile)
        user_serializer = UserProfileSerializer(request.user)
        return Response({'user': user_serializer.data, 'profile': serializer.data}, status=status.HTTP_200_OK)
