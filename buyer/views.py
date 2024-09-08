from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from accounts.renderers import UserRenderer
from .serializers import BuyerProfileSerializer
from accounts.serializers import UserProfileSerializer
from .models import Profile
from rest_framework.generics import RetrieveAPIView

class BuyerProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = BuyerProfileSerializer(data=request.data, context={'user': request.user, 'verify': True})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Buyer profile created!"}, status=status.HTTP_201_CREATED)
    
    def get(self, request, *args, **kwargs):
        buyer_profile = Profile.objects.get(user=request.user)
        serializer = BuyerProfileSerializer(buyer_profile)
        user_serializer = UserProfileSerializer(request.user)
        return Response({'user': user_serializer.data, 'profile': serializer.data}, status=status.HTTP_200_OK)

class BuyerProfileDetailView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = BuyerProfileSerializer
    lookup_field = 'user__id'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        buyer_profile = self.get_queryset().first()
        serializer = self.get_serializer(buyer_profile)
        user_serializer = UserProfileSerializer(request.user)
        return Response({'user': user_serializer.data, 'profile': serializer.data}, status=status.HTTP_200_OK)
