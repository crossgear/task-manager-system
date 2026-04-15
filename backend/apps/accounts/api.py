from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer
from django.contrib.auth.models import User


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({'detail': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'detail': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data.get('username'), 
            password=request.data.get('password')
            )

        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class LogoutView(APIView):
    def post(self, request):
        if request.auth:
            request.auth.delete()
            return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Not active session'}, status=status.HTTP_401_UNAUTHORIZED)        