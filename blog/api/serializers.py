from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Category, Post, Tag, Comment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# ----- User Serializer -----
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

# ----- Category Serializer -----
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

# ----- Tag Serializer -----
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

# ----- Post Serializer -----
class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'likes', 'dislikes', 'author']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

# ----- Comment Serializer -----
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'likes', 'dislikes', 'replies', 'parent']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

    def validate_content(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Content cannot be blank.")
        return value

   

    def validate_content(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Content cannot be blank.")
        return value

# ----- JWT Custom Serializer -----
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username  
        return data
