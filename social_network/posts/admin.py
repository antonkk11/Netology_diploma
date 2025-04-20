from django.contrib import admin
from .models import Post, Like, Comment, PostImage

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'author__username')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'author__username')


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'created_at')
    list_filter = ('created_at',)
