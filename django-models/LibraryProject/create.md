# Import the Book model from the bookshelf app
from bookshelf.models import Book

# Create and save a new Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# The book is now saved in the database.
# Expected output: A Book object is created and returned.
# You can verify by printing the object:
print(book)
# Expected output: 1984