from django.core.mail import message 
from django.shortcuts import redirect, render
from rest_framework import generics,permissions, status,views 
from rest_framework import serializers

from rest_framework.serializers import Serializer
from .serializers import*
from rest_framework.response import Response 
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
# from .utils import*
from .renderers import*



# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class=RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user=request.data 
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data=serializer.data
        user=User.objects.get(email=user_data['email'])
        #getting the registration token to permit the user
        token=RefreshToken.for_user(user).access_token #method  to get 
        #access token

        #i dont need to send averify user or user activation link.
        return Response(user_data,status=status.HTTP_201_CREATED)
