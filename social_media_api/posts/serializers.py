from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

# Post ViewSet for CRUD operations
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Only owners can edit or delete

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
