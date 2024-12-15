from rest_framework import viewsets, permissions, filters, generics, status, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from notifications.models import Notification

class PostPagination(PageNumberPagination):
    page_size = 10

# Post ViewSet for CRUD operations
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Only owners can edit or delete
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']  # Allow search by title and content
    pagination_class = PostPagination

    def perform_create(self, serializer):
        """
        Set the author to the current authenticated user.
        """
        serializer.save(author=self.request.user)

# Comment ViewSet for CRUD operations
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Only owners can edit or delete

    def perform_create(self, serializer):
        """
        Set the author to the current authenticated user.
        """
        post = self.request.data.get('post')  # Get the post from the request data
        serializer.save(author=self.request.user, post_id=post)


class FeedView(generics.ListAPIView):
    """
    View that returns posts from users the current user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author__in=user.following.all()).order_by('-created_at')
    
CustomUser = get_user_model()  # Custom User model

class FeedView(generics.GenericAPIView):
    """
    A view to display posts from users the current user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access

    def get(self, request, *args, **kwargs):
        user = request.user  # Get the current logged-in user

        # Fetch the users the current user is following
        following_users = user.following.all()  # Assumes 'following' is a ManyToMany field in CustomUser

        # Filter posts authored by followed users, ordered by creation date
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        # Serialize the posts
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
class LikePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Get the post or return 404
        post = generics.get_object_or_404(Post, pk=pk)

        # Create or get a like (prevents duplicates)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            # Create a notification only if a new like is made
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )
            return Response({"message": "Post liked successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You have already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

class UnlikePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Get the post or return 404
        post = generics.get_object_or_404(Post, pk=pk)

        # Check if the like exists
        like = Like.objects.filter(user=request.user, post=post)
        if like.exists():
            # Delete the like
            like.delete()
            return Response({"message": "Post unliked successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You haven't liked this post yet"}, status=status.HTTP_400_BAD_REQUEST)