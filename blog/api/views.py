from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from django.core.mail import send_mail
from rest_framework import generics, permissions
from blog.models import Comment


from .serializers import CommentSerializer

from ..models import Post, Category
from .serializers import UserSerializer, PostSerializer, CategorySerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': {'username': user.username, 'email': user.email},
            'token': token.key,
            'message': 'User created successfully.'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def view_add_post(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        ordering = request.GET.get('ordering', '-publish_date')
        try:
            posts = posts.order_by(ordering)
        except Exception:
            posts = posts.order_by('-publish_date')

        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_posts = paginator.paginate_queryset(posts, request)
        serialized = PostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serialized.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required to add post."},
                            status=status.HTTP_401_UNAUTHORIZED)
        created_post = PostSerializer(data=request.data)
        created_post.is_valid(raise_exception=True)
        created_post.save(author=request.user)
        return Response(created_post.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])  # Make GET public, but restrict others to auth below
def post_by_id(request, id):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serialized_post = PostSerializer(post)
        return Response(serialized_post.data, status=status.HTTP_200_OK)

    # For methods modifying data, require authentication:
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method in ['PUT', 'PATCH']:
        is_partial = request.method == 'PATCH'
        edited_post = PostSerializer(post, data=request.data, partial=is_partial)
        edited_post.is_valid(raise_exception=True)
        edited_post.save(author=request.user)
        return Response(edited_post.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    categories = Category.objects.all()
    serialized = CategorySerializer(categories, many=True, context={'request': request})
    return Response(serialized.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_posts_by_category_id(request, id):
    try:
        category = Category.objects.get(pk=id)
    except Category.DoesNotExist as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    posts = category.post_set.all().order_by('-publish_date')

    paginator = PageNumberPagination()
    paginator.page_size = 5
    paginated = paginator.paginate_queryset(posts, request)
    serialized = PostSerializer(paginated, many=True)
    return paginator.get_paginated_response(serialized.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_to_category(request):
    category_id = request.data.get('category_id')
    if not category_id:
        return Response({'error': 'Category ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    request.user.subscribed_categories.add(category)

    send_mail(
        'Subscription Confirmation',
        f'You have successfully subscribed to category: {category.name}',
        'noreply@yourblog.com',
        [request.user.email],
        fail_silently=True,
    )

    return Response({'message': f'Subscribed to category: {category.name}'}, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unsubscribe_from_category(request):
    category_id = request.data.get('category_id')
    if not category_id:
        return Response({'error': 'Category ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    request.user.subscribed_categories.remove(category)  # Adjust according to your User model's relation
    return Response({'message': f'Unsubscribed from category: {category.name}'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_subscriptions(request):
    user = request.user
    categories = user.subscribed_categories.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def all_categories_with_subscription_status(request):
    user = request.user
    if user.is_authenticated:
        user_subscribed_ids = set(user.subscribed_categories.values_list('id', flat=True))
    else:
        user_subscribed_ids = set()

    categories = Category.objects.all()
    data = []

    for category in categories:
        data.append({
            'id': category.id,
            'name': category.name,
            'subscribed': category.id in user_subscribed_ids,
        })

    return Response(data, status=200)

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(user=self.request.user, post_id=post_id)
