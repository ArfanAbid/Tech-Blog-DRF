from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from .serializers import *
from .models import BlogModel
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from rest_framework import filters

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    '''
    API endpoint for accessing the blog List
    '''
    def get(self, request, *args, **kwargs):
        try:
            query=BlogModel.objects.filter(user_id=request.user)
            # search
            if request.GET.get('search'):
                search=request.GET.get('search')
                query=query.filter(Q(title__icontains=search)|Q(content__icontains=search))

            serializer=BlogSerializer(query, many=True)
            return Response({'message':'Blogs fetched Successfully','data':serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    '''
    API endpoint for creating a blog
    '''
    def post(self, request, *args, **kwargs):
        try:
            data=request.data

            data['user_id']=request.user.id        # print(request.user) actually here we set uid as PK and user_id as FK bec it is child class of BaseModel so now here uid will automatically be provided and we have to set user_id manually which we set to id in a db of User  
            data['ownerName']=request.user.username 
            serializer=BlogSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'message':'Blog Created Successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
            

    '''
    API endpoint for updating a blog
    '''
    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            uid_request = data.get('uid')
            blog_instance = BlogModel.objects.get(uid=uid_request)
            
            # Ensure the user has permission to update this blog
            if request.user != blog_instance.user_id:
                return Response({'message': 'You do not have permission to update this blog'}, status=status.HTTP_403_FORBIDDEN)
            
        except BlogModel.DoesNotExist:# if blog_instance is None
            return Response({'message': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            serializer = BlogSerializer(blog_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data, 'message': 'Blog Updated Successfully'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    '''
    API endpoint for deleting a blog
    ''' 

    def delete(self, request, *args, **kwargs):
        try:
            data = request.data
            uid_request = data.get('uid')
            blog_instance = BlogModel.objects.get(uid=uid_request)
            
            # Ensure the user has permission to delete this blog
            if request.user != blog_instance.user_id:
                return Response({'message': 'You do not have permission to delete this blog'}, status=status.HTTP_403_FORBIDDEN)
            
        except BlogModel.DoesNotExist:# if blog_instance is None
            return Response({'message': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            blog_instance.delete()
            return Response({'message': 'Blog Deleted Successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


'''
API endpoint for listing blog unauthenticated users
'''

class BlogList(generics.ListAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]  
    
    queryset=BlogModel.objects.all().order_by('?')    # For random data
    serializer_class = BlogSerializer

    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['title__icontains', 'content__icontains']
    ordering_fields = ['title']