"""
URL configuration for django_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from blog import views as blog_views
from django.contrib.auth import views as authView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Include auth URLs
    path('login/', authView.LoginView.as_view(template_name='template/login.html'), name='login'),
    path('logout/', authView.LogoutView.as_view(), name='logout'),
    path('register/', authView.LoginView.as_view(template_name='template/register.html'), name='register'),
    path('profile/', authView.LoginView.as_view(template_name='template/profile.html'), name='profile'),
    path('', blog_views.home, name='home'),  # Add a root URL pointing to the home view
]
