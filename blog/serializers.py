
from rest_framework import serializers
from .models import Category, Subscription

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'category']

# If you have a Post model, add its serializer as well:
try:
    from .models import Post

    class PostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ['id', 'title', 'content', 'category', 'author', 'created_at']
except ImportError:
    pass
