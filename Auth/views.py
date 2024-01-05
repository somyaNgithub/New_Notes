from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from django.contrib.auth.hashers import check_password

# Create your views here.

#-----view to POST user details (registration)-----
@api_view(['POST'])
def signup(request):
    deserializer = CustomUserSerializer(data=request.data)
    print(deserializer)
    
    if deserializer.is_valid():
        user = deserializer.save()  # Save the user instance
        refresh = RefreshToken.for_user(user)
        data2= deserializer.data
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user':data2
        }
        return Response({'data':data, 'api_status':True}, status=status.HTTP_201_CREATED)
    else:
        # If the data is not valid, return validation errors
        return Response({'errors': deserializer.errors}, status=status.HTTP_400_BAD_REQUEST)




#-----view to post username and password (login)-----
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(password)

    # Ensure both username and password are provided
    if not username or not password:
        return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve the user by username
    user = CustomUser.objects.filter(userName__iexact=username).first()
    print(user.password)
    
    if user and check_password(password, user.password):
        # Password is correct
        # deserialize the user data(converting JSON into django models )
        
        deserializer = CustomUserSerializer(user)
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
      
        return Response({
            'Token':data,
            'user': deserializer.data,
            'api_status':True
        })
    else:
        # Invalid username or password
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
