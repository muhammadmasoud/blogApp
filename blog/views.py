from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Comment, Post,Category
from .serializers import CommentSerializer, PostSerializer,CategorySerializer

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]

@api_view (['GET' , 'POST'])
def view_add_post (request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serialized_posts = PostSerializer (instance=posts , many=True)
        return Response(data=serialized_posts.data , status=status.HTTP_200_OK)
    if request.method == 'POST':
        created_post = PostSerializer(data=request.data)
        #Automatically returns bad request if the post is invalid
        created_post.is_valid(raise_exception=True)
        # created_post.save()
        created_post.save(author=request.user)
        return Response(created_post.data , status=status.HTTP_201_CREATED)

@api_view(['GET' , 'PUT' , 'PATCH' , 'DELETE'])
def post_by_id(request,id):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist as e:
        return Response({"error":str(e)},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serialized_post = PostSerializer(instance = post)
        return Response(serialized_post.data , status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        if request.method == 'PUT':
            edited_post = PostSerializer(instance=post, data=request.data)
        elif request.method == 'PATCH':
            edited_post = PostSerializer(instance=post, data=request.data, partial=True)

        edited_post.is_valid(raise_exception=True)
        # edited_post.save()
        edited_post.save(author=request.user)
        return Response(data=edited_post.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
#Returns all categories
def get_categories(request):
    categories = Category.objects.all()
    serialized_categories = CategorySerializer(instance=categories,many=True)
    return Response(data=serialized_categories.data , status=status.HTTP_200_OK)

@api_view(['GET'])
#Returns all posts under a certain category given its id
def get_posts_by_category_id(request,id):
    try:
        category = Category.objects.get(pk=id)
    except Category.DoesNotExist as e:
        return Response({"error":str(e)},status=status.HTTP_404_NOT_FOUND)
    
    category_posts = category.post_set.all()
    serialized_posts = PostSerializer(instance=category_posts, many=True)
    return Response(serialized_posts.data, status=status.HTTP_200_OK)

