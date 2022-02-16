from django.core.mail import message 
from django.shortcuts import redirect, render
from rest_framework import generics,permissions, status,views 
from rest_framework import serializers

from rest_framework.views import APIView
from rest_framework.serializers import Serializer
from .serializers import*
from rest_framework.response import Response 
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .utils import*
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


class LoginAPIView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data 
        user = User.objects.get(email=user_data['email'])

        #on login i intend to send an email to user to welcome them back
        email_body='Welcome\t+\t'+user.username.upper()+',we are glad to have u back. '
        data={
            'email_body':email_body,
            'to_email':user.email,
            'email_subject':'Login Successful'
        }
        Util.send_email(data)

        return Response(serializer.data,status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    #since to logout on ehas to be authenticated.
    permission_classes = (permissions.IsAuthenticated,)#it has to be atuple

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

#just found out another view which is aswell similar to the above for logout

class LogoutView(APIView):
    permission_classes =(permissions.IsAuthenticated,)

    def post(self,request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)