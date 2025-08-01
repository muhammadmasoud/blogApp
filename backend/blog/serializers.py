from rest_framework import serializers
from .models import Comment, Category , Post, Tag, Subscription
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_blocked = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm', 'is_admin', 'is_blocked']
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
    user = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'replies', 'parent']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

    def validate_content(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Content cannot be blank.")
        return value

class CategorySerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'subscribed']

    def get_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        if user and user.is_authenticated:
            return obj.subscription_set.filter(user=user).exists()
        return False

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()
    liked_by_me = serializers.SerializerMethodField()
    disliked_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'likes', 'dislikes', 'author']

    def get_author(self, obj):
        return {
            "id": obj.author.id,
            "username": obj.author.username
        }

    def get_liked_by_me(self, obj):
        request = self.context.get('request', None)
        if request and request.user and request.user.is_authenticated:
            from blog.models import PostLike
            return PostLike.objects.filter(post=obj, user=request.user, is_like=True).exists()
        return False

    def get_disliked_by_me(self, obj):
        request = self.context.get('request', None)
        if request and request.user and request.user.is_authenticated:
            from blog.models import PostLike
            return PostLike.objects.filter(post=obj, user=request.user, is_like=False).exists()
        return False

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'category']

# If you have a Post model, add its serializer as well:
# Removed duplicate PostSerializer here to avoid override issues.

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['is_admin'] = getattr(self.user, 'is_admin', False)
        return data


