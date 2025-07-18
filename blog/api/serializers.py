from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Category, Post, Tag

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
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# ----- Tag Serializer -----
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

# ----- Post Serializer -----
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
