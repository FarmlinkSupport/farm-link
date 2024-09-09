from rest_framework import views, status,permissions
from .serializers import DraftSerializer,DraftGetSerializer,DraftUpdateBuyerSerializer
from rest_framework.response import Response
from accounts.renderers import UserRenderer
from .models import Draft
from tender.models import Tender
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

class DraftCreateListView(views.APIView):
    permission_classes=[permissions.IsAuthenticated]
    renderer_classes=[UserRenderer]

    def post(self,request,*args,**kwargs):
        if request.user.role !=1:
            return HttpResponse('You are not authorized to view this page content')
        serializer=DraftSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tender_id=self.kwargs['tender_id']
        draft=serializer.save(tender_id=tender_id,user=request.user)
        return Response(draft,status=status.HTTP_201_CREATED)
    
    def get(self,request,*args,**kwargs):
        id=self.kwargs['tender_id']
        tender=Tender.objects.get(id=id)
        drafts=Draft.objects.filter(tender=tender)
        serializer=DraftGetSerializer(drafts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class DraftUpdateRetrieveDestroyView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get(self,request,id,*args,**kwargs):
        draft=Draft.objects.get(id=id)
        if draft is None:
            return Response('Darft id is wrong please check it',status=status.HTTP_404_NOT_FOUND)
        serializer=DraftGetSerializer(draft,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,id,*args,**kwargs):
        draft=Draft.objects.get(id=id)
        if draft is not None:
            return Response('Darft id is wrong please check it',status=status.HTTP_404_NOT_FOUND)
        if draft.farmer != request.user:
            return Response("You are not allowed to update the draft",status=status.HTTP_403_FORBIDDEN)
        serializer=DraftSerializer(draft,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    
    def delete(self,request,id,*args,**kwargs):
        draft=Draft.objects.get(id=id)
        if draft is not None:
            return Response('Darft id is wrong please check it',status=status.HTTP_404_NOT_FOUND)
        if draft.farmer != request.user:
            return Response("You are not allowed to update the draft",status=status.HTTP_403_FORBIDDEN)
        draft.delete()
        return Response({"message": "Tender deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class DraftStatusUpdateView(views.APIView):
    permission_classes=[permissions.IsAuthenticated]
    renderer_classes=[UserRenderer]

    def put(self,request,id,*args,**kwargs):
        draft=Draft.objects.get(id=id)
        if draft is not None:
            return Response('Darft id is wrong please check it',status=status.HTTP_404_NOT_FOUND)
        if draft.tender.company_id != request.user:
            return PermissionDenied('You are not allowed to update the draft')
        serializer=DraftUpdateBuyerSerializer(draft,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)

