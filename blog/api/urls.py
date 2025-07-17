from django.urls import path
from .views import view_add_post

urlpatterns = [
    path ('api/posts/' , view_add_post)
]