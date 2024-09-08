from rest_framework import views, status, permissions
from rest_framework.response import Response
from asgiref.sync import sync_to_async
from .serializers import DraftSerializer, DraftGetSerializer, DraftUpdateBuyerSerializer
from .models import Draft
from tender.models import Tender
from accounts.renderers import UserRenderer
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

class DraftCreateListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    async def post(self, request, *args, **kwargs):
        if request.user.role != 1:
            return HttpResponse('You are not authorized to view this page content')
        serializer = DraftSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tender_id = request.data['id']
        tender= await sync_to_async(Tender.objects.get)(id=tender_id)
        draft= await sync_to_async(Draft.objects.get)(tender=tender,farmer=request.user)
        if draft is not None:
            return Response({'Draft has already been posted!!'},status=status.HTTP_226_IM_USED)
        await sync_to_async(serializer.save)(tender_id=tender_id, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    async def get(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        if not id:
            return Response({'error': 'ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        tender = await sync_to_async(Tender.objects.get)(id=id)
        drafts = await sync_to_async(Draft.objects.filter)(tender=tender)
        serializer = DraftGetSerializer(drafts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DraftUpdateRetrieveDestroyView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    async def get(self, request, id, *args, **kwargs):
        draft = await sync_to_async(Draft.objects.get)(id=id)
        if not draft:
            return Response('Draft id is wrong please check it', status=status.HTTP_404_NOT_FOUND)
        serializer = DraftGetSerializer(draft)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    async def put(self, request, id, *args, **kwargs):
        draft = await sync_to_async(Draft.objects.get)(id=id)
        if not draft:
            return Response('Draft id is wrong please check it', status=status.HTTP_404_NOT_FOUND)
        if draft.farmer != request.user:
            return Response("You are not allowed to update the draft", status=status.HTTP_403_FORBIDDEN)
        serializer = DraftSerializer(draft, data=request.data)
        serializer.is_valid(raise_exception=True)
        await sync_to_async(serializer.save)()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    async def delete(self, request, id, *args, **kwargs):
        draft = await sync_to_async(Draft.objects.get)(id=id)
        if not draft:
            return Response('Draft id is wrong please check it', status=status.HTTP_404_NOT_FOUND)
        if draft.farmer != request.user:
            return Response("You are not allowed to delete the draft", status=status.HTTP_403_FORBIDDEN)
        await sync_to_async(draft.delete)()
        return Response({"message": "Draft deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class DraftStatusUpdateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    async def put(self, request, id, *args, **kwargs):
        draft = await sync_to_async(Draft.objects.get)(id=id)
        if not draft:
            return Response('Draft id is wrong please check it', status=status.HTTP_404_NOT_FOUND)
        if draft.tender.company_id != request.user.id:
            raise PermissionDenied('You are not allowed to update the draft')
        serializer = DraftUpdateBuyerSerializer(draft, data=request.data)
        serializer.is_valid(raise_exception=True)
        await sync_to_async(serializer.save)()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
