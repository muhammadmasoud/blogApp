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
        created_post.save()
        return Response(created_post.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH'])
def post_by_id(request, id):
    pass  
