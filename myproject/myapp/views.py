from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import uuid


tokens = {}

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password)
    return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def authenticate_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        token = str(uuid.uuid4())
        tokens[token] = username  # Store token with associated username
        return Response({"token": token}, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def protected_resource(request):
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return Response({"error": "Missing authorization header."}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
    
    if token in tokens:
        return Response({"data": "This is protected content accessible to authenticated users."}, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid or missing authentication token."}, status=status.HTTP_401_UNAUTHORIZED)
