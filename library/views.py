import logging
from rest_framework.permissions import IsAuthenticated
from django.db import DatabaseError
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Book, BookDetails, BorrowedBooks
from .serializers import UserSerializer, BookSerializer, BookDetailsSerializer, BorrowedBookSerializer, UserBorrowedBooksSerializer

# Set up logging for error tracking and debugging
logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    # This line sets the queryset for this viewset to all User instances
    queryset = User.objects.all()
    # Specifies the serializer class to be used for serializing and deserializing data
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    

    # Custom create method to handle both single and bulk user creation
    def create(self, request, *args, **kwargs):
        try:
            # Check if the request data is a list for bulk creation
            if isinstance(request.data, list):
                # Get the serializer for the list of data with many=True
                serializer = self.get_serializer(data=request.data, many=True)
                # Validate the serializer data
                serializer.is_valid(raise_exception=True)
                # Save the validated data
                self.perform_create(serializer)
                # Generate success headers for the response
                headers = self.get_success_headers(serializer.data)
                # Return the serialized data with a 201 status code
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                # If the request data is not a list, proceed with default single create
                return super(UserViewSet, self).create(request, *args, **kwargs)
        except DatabaseError as e:
            # Log and handle database errors
            logger.error(f"Database error on user creation: {e}")
            return Response({"error": "Database error while creating user(s)."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Log and handle unexpected errors
            logger.error(f"Unexpected error on user creation: {e}")
            return Response({"error": "Unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookViewSet(viewsets.ModelViewSet):
    # Sets the queryset to all Book instances
    queryset = Book.objects.all()
    # Specifies the serializer class for books
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author']

    def create(self, request, *args, **kwargs):
        # The following logic mirrors that of the UserViewSet's create method
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super(BookViewSet, self).create(request, *args, **kwargs)

class BookDetailsViewSet(viewsets.ModelViewSet):
    # Sets the queryset to all BookDetails instances
    queryset = BookDetails.objects.all()
    # Specifies the serializer class for book details
    serializer_class = BookDetailsSerializer

    def create(self, request, *args, **kwargs):
        # Repeats the bulk creation logic used in UserViewSet and BookViewSet
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super(BookDetailsViewSet, self).create(request, *args, **kwargs)

class BorrowedBooksViewSet(viewsets.ModelViewSet):
    # Sets the queryset for borrowed books
    queryset = BorrowedBooks.objects.all()
    # Specifies the serializer class for borrowed books
    serializer_class = BorrowedBookSerializer
    
class UserBorrowedBooksListView(generics.ListAPIView):
    # Sets the queryset to all User instances for listing borrowed books
    queryset = User.objects.all()
    # Specifies the serializer class for listing borrowed books by user
    serializer_class = UserBorrowedBooksSerializer
    # You might consider adding filter backends here for more dynamic querying
