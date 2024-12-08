from django.urls import path, include
from django.contrib.auth import views as authView
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', authView.LoginView.as_view(template_name='template/login.html'), name='login'),
    path('logout/', authView.LogoutView.as_view(), name='logout'),

    # Custom Registration and Profile URLs
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),    
]
