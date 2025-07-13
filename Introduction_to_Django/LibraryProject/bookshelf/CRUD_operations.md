Django ORM CRUD Operations
This document details the CRUD (Create, Retrieve, Update, Delete) operations performed on the Book model via the Django shell (python manage.py shell).

Create Operation
Command: Create a Book instance with the title “1984”, author “George Orwell”, and publication year 1949.

# Import the Book model from the bookshelf app
from bookshelf.models import Book

# Create and save a new Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# The book is now saved in the database.
# Expected output: A Book object is created and returned.
# You can verify by printing the object:
print(book)
# Expected output: 1984

Retrieve Operation
Command: Retrieve and display all attributes of the book you just created.

# Import the Book model
from bookshelf.models import Book

# Retrieve the book with the title "1984"
book = Book.objects.get(title="1984")

# Display its attributes
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")

# Expected output:
# Title: 1984, Author: George Orwell, Year: 1949

Update Operation
Command: Update the title of “1984” to “Nineteen Eighty-Four” and save the changes.

# Import the Book model
from bookshelf.models import Book

# First, retrieve the book
book = Book.objects.get(title="1984")

# Update the title attribute
book.title = "Nineteen Eighty-Four"

# Save the changes to the database
book.save()

# Verify the update
updated_book = Book.objects.get(id=book.id)
print(updated_book.title)

# Expected output:
# Nineteen Eighty-Four

Delete Operation
Command: Delete the book you created and confirm the deletion.

# Import the Book model
from bookshelf.models import Book

# Retrieve the book to be deleted
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the object
result = book.delete()

# Confirm the deletion
print(result)

# Try to retrieve all books to confirm it's gone
all_books = Book.objects.all()
print(all_books)

# Expected output:
# The delete() method returns a tuple with the number of objects deleted.
# (1, {'bookshelf.Book': 1})
#
# The query for all books will return an empty QuerySet.
# <QuerySet []>
