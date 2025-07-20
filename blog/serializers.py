from rest_framework import serializers
from .models import Comment, Category , Post, Tag

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


