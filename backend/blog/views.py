from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import Comment, Post, Category, Subscription
from rest_framework.views import APIView
from django.core.mail import send_mail
from blog.models import Comment
from .serializers import (
    UserSerializer,
    PostSerializer,
    CategorySerializer,
    CommentSerializer,
    CustomTokenObtainPairSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def react_to_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    action = request.data.get('action')

    if action == 'like':
        comment.likes.add(request.user)
        comment.dislikes.remove(request.user)
    elif action == 'dislike':
        comment.dislikes.add(request.user)
        comment.likes.remove(request.user)
    else:
        return Response({'error': 'Invalid action'}, status=400)

    return Response({'message': f'{action.capitalize()} added'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reply_to_comment(request, comment_id):
    parent = get_object_or_404(Comment, id=comment_id)
    post = parent.post

    content = request.data.get('content')
    if not content:
        return Response({'error': 'Content is required'}, status=400)

    reply = Comment.objects.create(
        user=request.user,
        post=post,
        parent=parent,
        content=content
    )
    serializer = CommentSerializer(reply)
    return Response(serializer.data, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def react_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    action = request.data.get('action')

    if action not in ['like', 'dislike']:
        return Response({'error': 'Invalid action'}, status=400)

    from blog.models import PostLike

    try:
        post_like = PostLike.objects.get(user=request.user, post=post)
        if (action == 'like' and post_like.is_like) or (action == 'dislike' and not post_like.is_like):
            # User clicked the same reaction again, so remove it (toggle off)
            post_like.delete()
        else:
            # User switched reaction (like <-> dislike)
            post_like.is_like = (action == 'like')
            post_like.save()
    except PostLike.DoesNotExist:
        # No previous reaction, create new
        PostLike.objects.create(user=request.user, post=post, is_like=(action == 'like'))

    post.refresh_from_db()
    return Response(PostSerializer(post, context={'request': request}).data)

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

# -------------------- Authentication --------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {'username': user.username, 'email': user.email},
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'User created successfully.'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            if user.is_blocked:
                raise AuthenticationFailed('This user is blocked. Contact admin.')
        except User.DoesNotExist:
            pass  # Let serializer handle invalid user
        return super().post(request, *args, **kwargs)

# -------------------- Posts --------------------
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def view_add_post(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        search_query = request.GET.get('search', '').strip()
        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        ordering = request.GET.get('ordering', '-publish_date')
        posts = posts.order_by(ordering)
        
        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_posts = paginator.paginate_queryset(posts, request)
        serialized = PostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serialized.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required to add post."}, status=401)
        created_post = PostSerializer(data=request.data)
        created_post.is_valid(raise_exception=True)
        created_post.save(author=request.user)
        return Response(created_post.data, status=201)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def post_by_id(request, id):
    post = get_object_or_404(Post, pk=id)

    if request.method == 'GET':
        return Response(PostSerializer(post, context={'request': request}).data)

    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=401)

    if request.method == 'DELETE':
        post.delete()
        return Response(status=204)

    if request.method in ['PUT', 'PATCH']:
        is_partial = request.method == 'PATCH'
        serializer = PostSerializer(post, data=request.data, partial=is_partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data)

class PostPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all().order_by('-publish_date')
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['publish_date']

# -------------------- Categories --------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    categories = Category.objects.all().order_by('-created_at')
    serializer = CategorySerializer(categories, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_posts_by_category_id(request, id):
    category = get_object_or_404(Category, pk=id)
    posts = category.post_set.all().order_by('-publish_date')

    paginator = PageNumberPagination()
    paginator.page_size = 5
    paginated = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(paginated, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_to_category(request):
    category_id = request.data.get('category_id')
    if not category_id:
        return Response({'error': 'Category ID is required'}, status=400)

    category = get_object_or_404(Category, id=category_id)
    subscription, created = Subscription.objects.get_or_create(user=request.user, category=category)
    if created:
        # Send confirmation email with custom message
        send_mail(
            subject='Subscription Confirmation',
            message=f'Hello - {request.user.username} - you have subscribed successfully in - {category.name} - welcome aboard',
            from_email='no-reply@blogapp.com',
            recipient_list=[request.user.email],
            fail_silently=True
        )
        return Response({'message': f'Subscribed to category: {category.name}'})
    else:
        return Response({'message': f'Already subscribed to category: {category.name}'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unsubscribe_from_category(request):
    category_id = request.data.get('category_id')
    if not category_id:
        return Response({'error': 'Category ID is required'}, status=400)

    category = get_object_or_404(Category, id=category_id)
    Subscription.objects.filter(user=request.user, category=category).delete()
    return Response({'message': f'Unsubscribed from category: {category.name}'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_subscriptions(request):
    categories = request.user.subscribed_categories.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def all_categories_with_subscription_status(request):
    user = request.user
    if user.is_authenticated:
        from .models import Subscription
        subscribed_ids = set(
            Subscription.objects.filter(user=user).values_list('category_id', flat=True)
        )
    else:
        subscribed_ids = set()

    categories = Category.objects.all().order_by('-created_at')
    data = [
        {
            'id': category.id,
            'name': category.name,
            'subscribed': category.id in subscribed_ids,
        } for category in categories
    ]
    return Response(data)


class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        data = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin,
                'is_blocked': user.is_blocked,
            }
            for user in users
        ]
        return Response(data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def block_unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    action = request.data.get('action')
    if action == 'block':
        user.is_blocked = True
        user.save()
        return Response({'message': f'User {user.username} blocked.'})
    elif action == 'unblock':
        user.is_blocked = False
        user.save()
        return Response({'message': f'User {user.username} unblocked.'})
    else:
        return Response({'error': 'Invalid action.'}, status=400)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def promote_demote_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    action = request.data.get('action')
    if action == 'promote':
        user.is_admin = True
        user.save()
        return Response({'message': f'User {user.username} promoted to admin.'})
    elif action == 'demote':
        user.is_admin = False
        user.save()
        return Response({'message': f'User {user.username} demoted from admin.'})
    else:
        return Response({'error': 'Invalid action.'}, status=400)

