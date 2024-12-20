from django.urls import path, include
from django.contrib.auth import views as authView
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, 
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    PostByTagListView, search_posts
)


urlpatterns = [
    # Authentication URLs
    path('login/', authView.LoginView.as_view(template_name='template/login.html'), name='login'),
    path('logout/', authView.LogoutView.as_view(), name='logout'),

    # Custom Registration and Profile URLs
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'), 
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag'),
    path('search/', search_posts, name='search_posts'),

]
