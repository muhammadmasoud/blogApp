from rest_framework import serializers
from .models import Category, Subscription
from rest_framework import serializers
from .models import Comment

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
  
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user', 'post', 'parent']
        read_only_fields = ['id', 'created_at', 'user']

    def validate_parent(self, value):
        if value and value.parent:
            raise serializers.ValidationError('Only single-level replies are allowed.')
        return value 
