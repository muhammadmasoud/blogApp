from rest_framework import serializers
from ..models import Category , Post

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer (serializers.ModelSerializer):
    #POST,PUT,PATCH accept Category as id 
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id' , 'created_at' , 'likes' , 'dislikes'] #likes and dislikes could later be removed 
    
    #GET representation
    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        rep['category'] = instance.category.name if instance.category else None
        return rep

