# Delete the book
book = Book.objects.get(pk=book.pk)
book.delete()
# Output: (1, {'bookshelf.Book': 1})

# Confirm deletion
Book.objects.all()
# Output: <QuerySet []>