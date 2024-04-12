from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogModel

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=BlogModel
        fields=('uid','user_id','ownerName','title','content','image')  # OR exclude=('created_at','updated_at)
