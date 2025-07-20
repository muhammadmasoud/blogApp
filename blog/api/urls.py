from django.urls import path
from .views import view_add_post,post_by_id,get_categories,get_posts_by_category_id

urlpatterns = [
    path('api/posts/' , view_add_post),
    path('api/posts/<int:id>/' , post_by_id),
    path('api/posts/categories/',get_categories),
    path('api/posts/categories/<int:id>/',get_posts_by_category_id)
]