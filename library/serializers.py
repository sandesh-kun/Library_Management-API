from rest_framework import serializers
from .models import User, Book, BookDetails, BorrowedBooks

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model, includes all fields.
    """
    class Meta:
        model = User
        fields = '__all__'  # Serialize all fields from User model

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model, includes all fields.
    """
    class Meta:
        model = Book
        fields = '__all__'  # Serialize all fields from Book model

class BookDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for BookDetails model, includes all fields.
    """
    class Meta:
        model = BookDetails
        fields = '__all__'  # Serialize all fields from BookDetails model

class BorrowedBookSerializer(serializers.ModelSerializer):
    """
    Serializer for BorrowedBooks model, specifically selects a subset of fields.
    """
    class Meta:
        model = BorrowedBooks
        fields = ['BookID', 'BorrowDate', 'ReturnDate']  # Serialize specific fields

class UserBorrowedBooksSerializer(serializers.ModelSerializer):
    """
    Serializer for User model that includes additional field to show all borrowed books by the user.
    """
    borrowed_books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['UserID', 'Name', 'Email', 'MembershipDate', 'borrowed_books']  # Custom field added

    def get_borrowed_books(self, user):
        """
        Custom method to get all borrowed books for a user.
        
        :param user: User instance
        :return: Serialized data of all borrowed books for the user
        """
        try:
            borrowed_books = BorrowedBooks.objects.filter(UserID=user)
            return BorrowedBookSerializer(borrowed_books, many=True).data
        except BorrowedBooks.DoesNotExist:
            # Handling the case where the BorrowedBooks query fails
            return []  # Return an empty list if no BorrowedBooks found
