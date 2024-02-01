from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BookViewSet, BookDetailsViewSet, BorrowedBooksViewSet

# Initialize a default router
router = DefaultRouter()

# Registering the viewsets with the router
# This automatically generates routes for the standard actions (list, create, retrieve, update, partial_update, destroy)
router.register(r'users', UserViewSet)  # Routes for user operations
router.register(r'books', BookViewSet)  # Routes for book operations
router.register(r'bookdetails', BookDetailsViewSet)  # Routes for book detail operations
router.register(r'borrowedbooks', BorrowedBooksViewSet)  # Routes for borrowed book operations

# URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Include all routes from the default router
]
