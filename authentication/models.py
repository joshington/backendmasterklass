from django.db import models

# Create your models here.
from django.contrib.auth.models import(
    AbstractBaseUser, BaseUserManager,PermissionsMixin
)
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):
    def create_user(self,username, email, password=None):
        if username is None:
            raise TypeError('Users should have ausername')
        if email is None:
            raise TypeError('Users should have an email')
        user=self.model(username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should npt be none')
        user=self.create_user(username,email,password)
        user.is_superuser=True
        user.is_staff=True
        user.save()
        return user
#we can have auth_providers here forexample google and email i dont like facebook since it
#needs avpn
AUTH_PROVIDERS = {'google':'google','email':'email'}


#==now the user model ==
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255,unique=True,db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    creatd_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255,blank=False,
        null=False,default=AUTH_PROVIDERS.get('email')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects= UserManager()

    def __str__(self):
        return self.email

    #methods to return user tokens
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
#the refresh contains both the refersh and the access token.
