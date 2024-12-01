from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # Sample data
        self.book1 = Book.objects.create(title="Book 1", author="Author A", publication_year="2020-01-01")
        self.book2 = Book.objects.create(title="Book 2", author="Author B", publication_year="2021-01-01")
        
        # URLs for endpoints
        self.list_url = reverse('book-list')
        self.detail_url = lambda pk: reverse('book-detail', args=[pk])
    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    def test_retrieve_book(self):
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Book 1")
    def test_create_book(self):
        data = {
            "title": "Book 3",
            "author": "Author C",
            "publication_year": "2022-01-01"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "Book 3")
    def test_update_book(self):
        data = {
            "title": "Updated Book 1",
            "author": "Updated Author A",
            "publication_year": "2020-01-01"
        }
        response = self.client.put(self.detail_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book 1")
    def test_delete_book(self):
        response = self.client.delete(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url, {'author': 'Author A'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Author A')
    def test_search_books_by_title(self):
        response = self.client.get(self.list_url, {'search': 'Book 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book 1')
    def test_order_books_by_publication_year(self):
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Book 1")  # Oldest book
        self.assertEqual(response.data[1]['title'], "Book 2")  # Newest book
    def test_create_book_requires_authentication(self):
        self.client.logout()  # Simulate unauthenticated user
        data = {
            "title": "Book 3",
            "author": "Author C",
            "publication_year": "2022-01-01"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
