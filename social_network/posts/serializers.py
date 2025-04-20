from rest_framework import serializers
from .models import Post, Comment, Like, PostImage


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')
    
    class Meta:
        model = Comment
        fields = ['author', 'text', 'created_at']


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.id')
    images = PostImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'image', 'created_at', 'comments', 'likes_count', 'images']
    
    def get_likes_count(self, obj):
        return obj.likes.count()


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['text', 'image']
        
    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user']
