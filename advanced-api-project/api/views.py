from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Book
from .serializers import BookSerializer

'''# Custom permission: Read-only for unauthenticated users, full access for authenticated users
class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only access to unauthenticated users
        return request.user and request.user.is_authenticated  # Require authentication for write operations
'''
# ListView: Retrieve all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow unauthenticated users read-only access

# DetailView: Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow unauthenticated users read-only access

# CreateView: Add a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Allow only authenticated users to create

    def perform_create(self, serializer):
        # Custom validation or logic
        title = serializer.validated_data.get('title')
        if Book.objects.filter(title=title).exists():
            raise ValidationError({'title': 'A book with this title already exists.'})
        serializer.save()

# UpdateView: Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Allow only authenticated users to update

    def perform_update(self, serializer):
        # Custom logic (e.g., log updates)
        instance = serializer.save()
        print(f"Book updated: {instance.title}")

# DeleteView: Remove a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Allow only authenticated users to delete
