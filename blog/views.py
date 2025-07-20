from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Comment, Post, Category, Subscription
from .serializers import CommentSerializer, PostSerializer,CategorySerializer
from rest_framework.views import APIView
from django.core.mail import send_mail

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

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'is_admin', False)


class SubscribeCategory(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        subscription, created = Subscription.objects.get_or_create(user=request.user, category=category)
        if created:
            # Send subscription email
            send_mail(
                subject='Subscription Confirmation',
                message=f'You have subscribed to the category: {category.name}',
                from_email='no-reply@blogapp.com',
                recipient_list=[request.user.email],
                fail_silently=True
            )
        return Response({'detail': 'Subscribed successfully.'}, status=status.HTTP_201_CREATED)

# If you have a Post model, add a view to filter posts by category
from django.db.models import Q
try:
    from .models import Post

    class PostListByCategory(APIView):
        permission_classes = [permissions.AllowAny]

        def get(self, request):
            category_id = request.query_params.get('category_id')
            if category_id:
                posts = Post.objects.filter(category_id=category_id)
            else:
                posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
except ImportError:
    pass

class CategoryList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryCreate(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryUpdate(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDelete(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return Response({'detail': 'Category deleted.'}, status=status.HTTP_204_NO_CONTENT)

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

