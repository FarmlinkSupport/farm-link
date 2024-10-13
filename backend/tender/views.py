from rest_framework import generics, status,views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Tender
from .serializers import TenderSerializer
from accounts.renderers import UserRenderer
from buyer.models import Profile

class TenderListCreateView(generics.ListCreateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        profile=Profile.objects.get(user=self.request.user)
        print(self.request.user,self.request.user.role,profile.is_verified)
        if self.request.user.role == 2 and profile.is_verified==True:
            tender=serializer.save(company_id=self.request.user)
            return Response(tender,status=status.HTTP_201_CREATED)
        raise PermissionDenied('You are not allowed to issue tender')
        

class TenderRetrieveUpdateDestroyView(views.APIView):
    renderer_classes = [UserRenderer]
    
    def get_object(self, id):
        try:
            return Tender.objects.get(pk=id)
        except Tender.DoesNotExist:
            return Response('tender does not exist',status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id, format=None):
        tender = self.get_object(id)
        serializer = TenderSerializer(tender)
        print(tender)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        tender = self.get_object(id)
        if tender.company_id != request.user.id:
            raise PermissionDenied("You do not have permission to update this tender.")
        serializer = TenderSerializer(tender, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        tender = self.get_object(id)
        if tender.company_id != request.user.id:
            raise PermissionDenied("You do not have permission to delete this tender.")
        tender.delete()
        return Response({"message": "Tender deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class TenderGetBuyerView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        tender =  Tender.objects.filter(company_id=request.user)
        if tender is None:
            return Response("User has no issued Tender",status=status.HTTP_204_NO_CONTENT)
        serializer=TenderSerializer(tender,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)