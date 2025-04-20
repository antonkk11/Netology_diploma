from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/like/", views.LikeView.as_view(), name="post-like"),
    path("posts/<int:pk>/comment/", views.CommentView.as_view(), name="post-comment"),
    path("posts/<int:pk>/images/", views.PostImageView.as_view(), name="post-images"),
]
