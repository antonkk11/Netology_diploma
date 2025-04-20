from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Post, Comment, Like, PostImage
from .serializers import (
    PostSerializer, PostCreateSerializer, CommentSerializer, LikeSerializer, PostUpdateSerializer, PostImageSerializer
)


class PostListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer
    
    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"detail": f"Ошибка при создании поста: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostUpdateSerializer
        return PostSerializer
    
    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {"detail": "У вас нет разрешения на редактирование этого поста."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {"detail": "У вас нет разрешения на удаление этого поста."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            return Response({"detail": "Пост отмечен лайком."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Вы уже поставили лайк этому посту."}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        
        if like:
            like.delete()
            return Response({"detail": "Лайк удален."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Вы не ставили лайк этому посту."}, status=status.HTTP_404_NOT_FOUND)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        
        # Проверяем, является ли пользователь автором поста
        if post.author != request.user:
            return Response(
                {"detail": "У вас нет разрешения на добавление изображений к этому посту."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Получаем файл из запроса
        if 'image' not in request.FILES:
            return Response(
                {"detail": "Изображение не найдено в запросе."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image = request.FILES['image']
        
        # Создаем дополнительное изображение
        post_image = PostImage.objects.create(post=post, image=image)
        serializer = PostImageSerializer(post_image)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)