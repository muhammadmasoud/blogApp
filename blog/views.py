from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Category, Subscription
from .serializers import CategorySerializer, PostSerializer
from django.core.mail import send_mail


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
