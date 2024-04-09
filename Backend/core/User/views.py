from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate,login,logout


class UserRegister(APIView):
    """
    API endpoint that allows users to be registered.
    """

    def post(self, request, *args, **kwargs):
        try:
            serializer=RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Account created successfully'}, status=status.HTTP_201_CREATED)
            
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)    



class UserLogin(APIView):
    """
    API endpoint that allows users to login.
    """

    def post(self, request, *args, **kwargs):
        try:
            serializer=LoginSerializer(data=request.data)
            if serializer.is_valid():
                username=serializer.validated_data['username']
                password=serializer.validated_data['password']
                user=authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return Response({'message':'Successfully logged in'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message':'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)    
        

class UserLogout(APIView):
    """
    API endpoint that allows users to logout.
    """
    def post(self, request, *args, **kwargs):
        try:
            logout(request)
            return Response({'message':'Successfully logged out'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)