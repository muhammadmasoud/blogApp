from django.urls import path
from .views import (
    signup,
    view_add_post,
    post_by_id,
    get_categories,
    get_posts_by_category_id
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login', obtain_auth_token, name='api-login'),
    path('signup', signup, name='api-signup'),
    
    # Post endpoints
    path('api/posts/', view_add_post, name='api-posts'),
    path('api/posts/<int:id>/', post_by_id, name='api-post-detail'),

    # Category endpoints
    path('api/posts/categories/', get_categories, name='api-categories'),
    path('api/posts/categories/<int:id>/', get_posts_by_category_id, name='api-posts-by-category'),
]
