from django.urls import path
from .views import CommentListCreateView, CommentDeleteView

urlpatterns = [
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
] 