from base64 import urlsafe_b64decode
import email
from logging import exception
from multiprocessing import AuthenticationError
from django.http import request 
from rest_framework import serializers 
from .models import User 
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes, \
    DjangoUnicodeDecodeError
#force str => gives us ahuman readbale id

from django.urls import reverse
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode



#ofcourse i have to do the usual stuff of registration 
#signup signin
#no need for activation link after registration

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)

    class Meta:
        model = User
        fields = ['email','username','password']
    
    def validate(self,attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should only contain alphanumeric xters. ')
        return attrs
    
    def create(sself, validated_data):
        return User.objects.create_user(**validated_data)

#to login only leverage the email and password of the user
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=3)
    password = serializers.CharField(max_length=68,min_length=6,write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self,obj):
        user=User.objects.get(email=obj['email'])
        return {
            'access':user.tokens()['access'],#we use this format since it returns adictionary
            'refresh':user.tokens()['refresh']
        }
    #use this format to arrange the access and refresh tokens in amore systematic way.
    class Meta:
        model=User
        fields=['email','password','tokens']
    
    def validate(self,attrs):
        email=attrs.get('email', '')
        password=attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)

        user = auth.authenticate(email=email,password=password)
        if filtered_user_by_email.exists() and  \
            filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using'+ filtered_user_by_email[0].auth_provider
            ) 
        if not user:
            raise AuthenticationFailed('Invalid credentials try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        #i wont handle the verification here cz i want upon registration the user to be
        #automatically verified upon registration
        #==> may be am going to handle it later but not now
        return {
            'email':user.email,
            'tokens':user.tokens,
        }
        return super().validate(attrs)


#so incase user forgets their password they will request for areset link
class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(
        min_length=6,max_length=68, write_only=True)
    token=serializers.CharField(
        min_length=1, max_length=6,write_only=True)
    uidb64=serializers.CharField(
        min_length=1, write_only=True
    )
    class Meta:
        fields = ['password','token','uidb64']
    
    def validate(self,attrs):
        try:
            password=attrs.get('password')
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            id=force_str(urlsafe_base64_decode(uidb64))
            user= User.objects.get(id=id)

            #have to check if the token has not been used before.
            if not PasswordResetTokenGenerator.check_token(user,token):
                raise AuthenticationFailed('The reset link is inavlid', 401)
            user.set_password(password)
            user.save()
            return user
            #after user has provided their password we need to set it as their new 
            #password.
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid',401)
        return super().validate(attrs)

class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()

    default_error_messages={
        'bad_token':('Token is expired or invalid')
    }
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
        #we use blacklist to remove the token from the list
