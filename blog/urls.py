from django.urls import path
from .views import signup, CommentListCreateView, CommentDeleteView, view_add_post,post_by_id,get_categories,get_posts_by_category_id
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('api/posts/' , view_add_post),
    path('api/posts/<int:id>/' , post_by_id),
    path('api/posts/categories/',get_categories),
    path('api/posts/categories/<int:id>/',get_posts_by_category_id),
    path('api/login', obtain_auth_token, name='api-login'),
    path('api/signup', signup, name='api-signup'),
] 