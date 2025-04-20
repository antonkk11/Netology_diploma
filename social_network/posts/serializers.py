from rest_framework import serializers
from .models import Post, Comment, Like, PostImage
import os


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
    image = serializers.ImageField(required=True)
    
    class Meta:
        model = Post
        fields = ['text', 'image']
    
    def validate_image(self, image):
        # Проверка размера файла - не более 10 МБ
        if image.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Размер изображения не должен превышать 10 МБ")
        
        # Проверка типа файла
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        ext = os.path.splitext(image.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(
                f"Недопустимый формат изображения. Поддерживаемые форматы: {', '.join(valid_extensions)}"
            )
        
        return image


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['text']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user']
