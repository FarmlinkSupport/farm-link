from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from asgiref.sync import sync_to_async
from .models import Tender
from .serializers import TenderSerializer
from accounts.renderers import UserRenderer
from buyer.models import Profile

class TenderListCreateView(generics.ListCreateAPIView):
    serializer_class = TenderSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    async def get_queryset(self):
        # Using sync_to_async to make ORM queries asynchronous
        return await sync_to_async(Tender.objects.all)()

    async def perform_create(self, serializer):
        profile = await sync_to_async(Profile.objects.get)(user=self.request.user)
        if self.request.user.role == 2 and profile.is_verified:
            # Save method is still synchronous
            await sync_to_async(serializer.save)(company_id=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise PermissionDenied('You are not allowed to issue tender')


class TenderRetrieveUpdateDestroyView(views.APIView):
    renderer_classes = [UserRenderer]

    async def get_object(self, id):
        try:
            return await sync_to_async(Tender.objects.get)(pk=id)
        except Tender.DoesNotExist:
            return None

    async def get(self, request, id, format=None):
        tender = await self.get_object(id)
        if not tender:
            return Response('Tender does not exist', status=status.HTTP_400_BAD_REQUEST)
        serializer = TenderSerializer(tender)
        return Response(serializer.data, status=status.HTTP_200_OK)

    async def put(self, request, id, format=None):
        tender = await self.get_object(id)
        if not tender:
            return Response('Tender does not exist', status=status.HTTP_400_BAD_REQUEST)
        if tender.company_id != request.user.id:
            raise PermissionDenied("You do not have permission to update this tender.")
        serializer = TenderSerializer(tender, data=request.data)
        if serializer.is_valid():
            await sync_to_async(serializer.save)()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    async def delete(self, request, id, format=None):
        tender = await self.get_object(id)
        if not tender:
            return Response('Tender does not exist', status=status.HTTP_400_BAD_REQUEST)
        if tender.company_id != request.user.id:
            raise PermissionDenied("You do not have permission to delete this tender.")
        await sync_to_async(tender.delete)()
        return Response({"message": "Tender deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class TenderGetBuyerView(views.APIView):
    permission_classes = [IsAuthenticated]

    async def get(self,request,*args,**kwargs):
        tender = await sync_to_async(Tender.objects.filter)(company_id=request.user)
        if tender is None:
            return Response("User has no issued Tender",status=status.HTTP_204_NO_CONTENT)
        serializer=TenderSerializer(tender,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
