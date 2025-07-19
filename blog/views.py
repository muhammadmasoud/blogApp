from django.shortcuts import render
from rest_framework import generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# List all posts OR create a new post
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-publish_date')
    serializer_class = PostSerializer

# Retrieve, update, or delete a single post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# List or add comments for a specific post
class PostCommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        post = Post.objects.get(pk=post_id)
        serializer.save(post=post)

def admin_dashboard(request):
    return render(request, 'dashboard/index.html')



