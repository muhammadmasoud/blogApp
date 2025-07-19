from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Category, Post, Tag ,Comment
from rest_framework.pagination import PageNumberPagination


# ----- User Serializer -----
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

# ----- Category Serializer -----
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
   # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    #tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
     category = CategorySerializer(read_only=True)  # nested serializer for category
     tags = TagSerializer(many=True, read_only=True)

     class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'likes', 'dislikes', 'author']

def to_representation(self, instance):
        rep = super().to_representation(instance)
       # rep['category'] = instance.category.name if instance.category else None
       # rep['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return rep
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class PostPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'