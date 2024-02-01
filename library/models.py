from django.db import models

# 1. User Model
class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    MembershipDate = models.DateField()

    def __str__(self):
        return self.Name

# 2. Book Model
class Book(models.Model):
    Title = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=13, unique=True)
    PublishedDate = models.DateField()
    Genre = models.CharField(max_length=100)

    def __str__(self):
        return self.Title

# 3. BookDetails Model
class BookDetails(models.Model):
    DetailsID = models.AutoField(primary_key=True)
    Book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='details')
    NumberOfPages = models.IntegerField()
    Publisher = models.CharField(max_length=100)
    Language = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.Book.Title} Details"

# 4. BorrowedBooks Model
class BorrowedBooks(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    BookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    BorrowDate = models.DateField()
    ReturnDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.UserID.Name} borrowed {self.BookID.Title}"
