# Update the title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
# No output (save returns None)

# Verify update
updated = Book.objects.get(pk=book.pk)
print(updated)
# Output: Nineteen Eighty-Four by George Orwell (1949)