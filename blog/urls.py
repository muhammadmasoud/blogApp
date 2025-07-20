from django.urls import path
from .views import CustomTokenObtainPairView, CommentListCreateView, CommentDeleteView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    signup,
    view_add_post,
    post_by_id,
    get_categories,
    get_posts_by_category_id
    
)

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', signup, name='api-signup'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('comments/<int:comment_id>/reply/', views.reply_to_comment, name='reply-comment'),
    path('api/posts/' , view_add_post),
    path('api/posts/<int:id>/' , post_by_id),
    path('api/posts/categories/',get_categories),
    path('api/posts/categories/<int:id>/',get_posts_by_category_id),
    path('api/login', obtain_auth_token, name='api-login'),
    path('api/signup', signup, name='api-signup'),
    path('posts/', view_add_post, name='api-posts'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='post-comments'),
    path('categories/', get_categories, name='api-categories'),
    path('categories/<int:id>/posts/', get_posts_by_category_id, name='api-posts-by-category'),
    path('posts/categories/', views.all_categories_with_subscription_status, name='categories_with_subscription_status'),
    path('user/subscriptions/', views.user_subscriptions, name='user_subscriptions'),
    path('user/subscribe/', views.subscribe_to_category, name='subscribe_category'),
    path('user/unsubscribe/', views.unsubscribe_from_category, name='unsubscribe_from_category'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/<int:post_id>/react/', views.react_to_post, name='react-post'),

]
    