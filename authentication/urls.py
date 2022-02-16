from django.urls import path
from .views import*
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )

app_name='authentication'


urlpatterns = [
    path('register/',RegisterView.as_view(), name="register"),
]
