from django.urls import path, include
from django.contrib.auth import views as authView
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
)


urlpatterns = [
    # Authentication URLs
    path('login/', authView.LoginView.as_view(template_name='template/login.html'), name='login'),
    path('logout/', authView.LogoutView.as_view(), name='logout'),

    # Custom Registration and Profile URLs
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'), 
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('new/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),   
]
