from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from blog.models import Comment
from ..models import Post, Category
from .serializers import (
    UserSerializer,
    PostSerializer,
    CategorySerializer,
    CommentSerializer,
    CustomTokenObtainPairSerializer
)

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

# -------------------- Posts --------------------

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def view_add_post(request):
    if request.method == 'GET':
        posts = Post.objects.all()
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
        return Response(PostSerializer(post).data)

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
    categories = Category.objects.all()
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
    request.user.subscribed_categories.add(category)

    send_mail(
        'Subscription Confirmation',
        f'You have successfully subscribed to category: {category.name}',
        'noreply@yourblog.com',
        [request.user.email],
        fail_silently=True,
    )

    return Response({'message': f'Subscribed to category: {category.name}'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unsubscribe_from_category(request):
    category_id = request.data.get('category_id')
    if not category_id:
        return Response({'error': 'Category ID is required'}, status=400)

    category = get_object_or_404(Category, id=category_id)
    request.user.subscribed_categories.remove(category)
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
    subscribed_ids = set(user.subscribed_categories.values_list('id', flat=True)) if user.is_authenticated else set()

    categories = Category.objects.all()
    data = [
        {
            'id': category.id,
            'name': category.name,
            'subscribed': category.id in subscribed_ids,
        } for category in categories
    ]
    return Response(data)

# -------------------- Comments --------------------

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

    from blog.models import PostLike  # import your model

    is_like = action == 'like'
    post_like, created = PostLike.objects.update_or_create(
        user=request.user,
        post=post,
        defaults={'is_like': is_like}
    )
    return Response({'message': f'{action.capitalize()} saved'})
