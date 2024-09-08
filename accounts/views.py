from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, UserLoginSerializer
from asgiref.sync import sync_to_async

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    async def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Saving the user must stay synchronous due to Django ORM
        user = await sync_to_async(serializer.save)()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    async def post(self, request):
        print(request.data)
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = await sync_to_async(authenticate)(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            await sync_to_async(login)(request, user)
            return Response({'token': token, 'user': request.user.name, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
