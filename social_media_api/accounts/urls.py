from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, follow_user, unfollow_user

urlpatterns = [
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('profile/', UserDetailView.as_view(),name='user_detail'),
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
]