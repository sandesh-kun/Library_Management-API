import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django.db import DatabaseError
from rest_framework.decorators import api_view
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Book, BookDetails, BorrowedBooks
from .serializers import UserSerializer, BookSerializer, BookDetailsSerializer, BorrowedBookSerializer, UserBorrowedBooksSerializer
from django.http import JsonResponse

# Set up logging for error tracking and debugging
logger = logging.getLogger(__name__)

@api_view(['POST'])
def create_auth(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = AuthUser.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
    filterset_fields = ['Title']
    permission_classes = [IsAuthenticated]

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

class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
# View for all borrowed books
def borrowed_books_list(request):
    borrowed_books = BorrowedBooks.objects.all()
    data = {"borrowed_books": list(borrowed_books.values())}  
    return JsonResponse(data)

def user_list(request):
    users = User.objects.all()
    data = {"users": list(users.values())} 
    return JsonResponse(data)