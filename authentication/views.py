from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from authentication.serializer import UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
def signup_user(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "User Created"})


@api_view(["POST"])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
    token = AccessToken.for_user(user)
    response = Response({'message': 'Logged in successfully'},status=200)
    
    response.set_cookie(
        key='jwt',
        value=str(token),
        httponly=True,
        samesite='Strict', 
        max_age=365 * 24 * 60 * 60, 
    )
    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    response = Response({'message': 'Logged out successfully'},
    status=200)
    response.delete_cookie('jwt')
    return response

