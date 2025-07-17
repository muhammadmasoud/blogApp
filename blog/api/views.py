from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Post,Category
from .serializers import PostSerializer,CategorySerializer

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
        created_post.save()
        return Response(created_post.data , status=status.HTTP_201_CREATED)

@api_view(['GET' , 'PUT' , 'PATCH'])
def post_by_id(request,id):
    pass