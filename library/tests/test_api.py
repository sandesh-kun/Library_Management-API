from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from library.models import Book

class BookAPITest(APITestCase):
    def setUp(self):
        # Setup run before every test method.
        self.book = Book.objects.create(Title="API Test Book", ISBN="1234567890123", PublishedDate="2024-01-01", Genre="Test Genre")

    def test_get_book_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_book(self):
        url = reverse('book-list')
        data = {'Title': 'New Book', 'ISBN': '1234567890123', 'PublishedDate': '2024-01-01', 'Genre': 'Fiction'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

