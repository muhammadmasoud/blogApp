from django.urls import path
from .views import CommentListCreateView
from . import views

from .views import (
    signup,
    view_add_post,
    post_by_id,
    get_categories,
    get_posts_by_category_id
    
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token, name='api-login'),
    path('signup/', signup, name='api-signup'),

    # Post endpoints
    path('posts/', view_add_post, name='api-posts'),
    path('posts/<int:id>/', post_by_id, name='api-post-detail'),

    # Category endpoints
    path('categories/', get_categories, name='api-categories'),
    path('categories/<int:id>/posts/', get_posts_by_category_id, name='api-posts-by-category'),

    # ✅ Fix these two
    path('posts/categories/', views.all_categories_with_subscription_status, name='categories_with_subscription_status'),
    path('user/subscriptions/', views.user_subscriptions, name='user_subscriptions'),

    # Subscription
    path('user/subscribe/', views.subscribe_to_category, name='subscribe_category'),
    path('user/unsubscribe/', views.unsubscribe_from_category, name='unsubscribe_from_category'),

     path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='post-comments'),
]
