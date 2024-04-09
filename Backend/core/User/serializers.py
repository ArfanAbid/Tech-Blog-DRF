from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    '''
    serializer for RegisterUser
    '''
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    username=serializers.CharField(max_length= 100, required=True)
    email=serializers.EmailField(required=True)
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True) # in DRF you can include a "confirm password" field in your serializer without it being a part of the actual User model

    def validate(self,data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'Error': 'Username already exists'})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'Error': 'Email already exists'})
        
        if data['password']!=data['confirm_password']:
            raise serializers.ValidationError({'Error': 'Passwords do not match'})

        return data
    

    def create(self, data):
        user=User.objects.create_user(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.set_password(data['password']) # for hashing passwords
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    '''
    serializer for LoginUser
    '''
    username=serializers.CharField(max_length= 100, required=True)
    password=serializers.CharField(write_only=True)

    def validate(self,data):
        username=data.get('username')
        password=data.get('password')

        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError( {'Error':'Username does not exist'})
        
        user=User.objects.get(username=username)
        if not user.check_password(password):
            raise serializers.ValidationError({'Error':'Incorrect password!'})
        
        return data
