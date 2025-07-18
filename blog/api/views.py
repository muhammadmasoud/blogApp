from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

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
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'token': token.key,
            'message': 'User created successfully.'
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def view_add_post(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serialized_posts = PostSerializer(instance=posts, many=True)
        return Response(data=serialized_posts.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        created_post = PostSerializer(data=request.data)
        created_post.is_valid(raise_exception=True)
        created_post.save(author=request.user)
        return Response(created_post.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def post_by_id(request, id):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serialized_post = PostSerializer(instance=post)
        return Response(serialized_post.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method in ['PUT', 'PATCH']:
        is_partial = request.method == 'PATCH'
        edited_post = PostSerializer(instance=post, data=request.data, partial=is_partial)
        edited_post.is_valid(raise_exception=True)
        edited_post.save(author=request.user)
        return Response(data=edited_post.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serialized_categories = CategorySerializer(instance=categories, many=True)
    return Response(data=serialized_categories.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_posts_by_category_id(request, id):
    try:
        category = Category.objects.get(pk=id)
    except Category.DoesNotExist as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    category_posts = category.post_set.all()
    serialized_posts = PostSerializer(instance=category_posts, many=True)
    return Response(serialized_posts.data, status=status.HTTP_200_OK)
