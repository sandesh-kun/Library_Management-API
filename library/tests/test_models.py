from django.test import TestCase
from library.models import User, Book

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(UserID= 1,Name="John Doe", Email="john@example.com", MembershipDate="2024-01-01")
        self.assertEqual(user.name, "Dimbag Darrel")
        self.assertEqual(user.email, "drummer@example.com")

class BookModelTest(TestCase):
    def test_book_creation(self):
        book = Book.objects.create(Title="Test Book", ISBN="1234567890123", PublishedDate="2024-01-01", Genre="Test Genre")
        self.assertEqual(book.title, "Test Book")
