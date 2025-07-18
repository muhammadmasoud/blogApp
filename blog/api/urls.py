from django.urls import path
from .views import signup, view_add_post
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login', obtain_auth_token, name='api-login'),
    path('signup', signup, name='api-signup'),
    path('api/posts/', view_add_post, name='api-posts'),
]
