from django.urls import path
from .views import*
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenObtainPairView
)

app_name='authentication'


urlpatterns = [
    path('register/',RegisterView.as_view(), name="register"),
    path('login/',LoginAPIView.as_view(), name="login"),
    path('login/refresh',TokenRefreshView.as_view(), name="token_refresh"),
    path('logout/',LogoutAPIView.as_view(), name="logout"),
]
