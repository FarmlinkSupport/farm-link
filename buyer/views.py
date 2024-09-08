from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from accounts.renderers import UserRenderer
from .serializers import BuyerProfileSerializer
from accounts.serializers import UserProfileSerializer
from .models import Profile
from rest_framework.generics import RetrieveAPIView
from asgiref.sync import sync_to_async


class BuyerProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    async def post(self, request, *args, **kwargs):
        # The serializer can be async since it's not bound by Django's ORM limitations
        serializer = BuyerProfileSerializer(data=request.data, context={'user': request.user, 'verify': True})
        serializer.is_valid(raise_exception=True)
        # ORM save is still synchronous, so we'll keep it like this for now
        serializer.save()
        return Response({"message": "Buyer profile created!"}, status=status.HTTP_201_CREATED)
    
    async def get(self, request, *args, **kwargs):
        # Django ORM is synchronous, so this must stay synchronous
        buyer_profile = await sync_to_async(Profile.objects.get)(user=request.user)
        serializer = BuyerProfileSerializer(buyer_profile)
        user_serializer = UserProfileSerializer(request.user)
        return Response({'user': user_serializer.data, 'profile': serializer.data}, status=status.HTTP_200_OK)


class BuyerProfileDetailView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = BuyerProfileSerializer
    lookup_field = 'user__id'

    async def get_queryset(self):
        return await sync_to_async(Profile.objects.filter)(user=self.request.user)

    async def retrieve(self, request, *args, **kwargs):
        buyer_profile = await sync_to_async(self.get_queryset().first)()
        serializer = self.get_serializer(buyer_profile)
        user_serializer = UserProfileSerializer(request.user)
        return Response({'user': user_serializer.data, 'profile': serializer.data}, status=status.HTTP_200_OK)
