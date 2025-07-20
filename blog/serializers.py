from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user', 'post', 'parent']
        read_only_fields = ['id', 'created_at', 'user']

    def validate_parent(self, value):
        if value and value.parent:
            raise serializers.ValidationError('Only single-level replies are allowed.')
        return value 