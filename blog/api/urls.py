from django.urls import path
from .views import signup
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('api/login', obtain_auth_token, name='api-login'),
    path('api/signup', signup, name='api-signup'),
]