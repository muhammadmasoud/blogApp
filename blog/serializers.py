from rest_framework import serializers
from .models import Comment, Category , Post, Tag, Subscription
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': "Passwords do not match"
            })
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user', 'post', 'parent']
        read_only_fields = ['id', 'created_at', 'user']

    def validate_parent(self, value):
        if value and value.parent:
            raise serializers.ValidationError('Only single-level replies are allowed.')
        return value 

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'likes', 'dislikes', 'author']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = instance.category.name if instance.category else None
        rep['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return rep

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


