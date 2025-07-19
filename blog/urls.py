from django.urls import path
from .views import PostListCreateView, PostDetailView, PostCommentsView , admin_dashboard


urlpatterns = [
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('api/posts/<int:pk>/comments/', PostCommentsView.as_view(), name='post-comments'),
    path('dashboard/', admin_dashboard, name='dashboard'),
]


