from django.db import models

# In Django, a "model" describes the structure of the data in the database
# (like a blueprint for a table — it says what fields exist and how they relate).
# A "serializer" is used to convert model data into formats like JSON (for APIs),
# and also to turn incoming data (like from a web form or request) back into a model.
# Adding comments that explain what each specific model and serializer is for
# makes it easier for anyone reading the code to quickly understand the purpose
# of each one without having to guess or read through all the logic.


class Author(models.Model):
    name = models.CharField(max_length=225)

class Book(models.Model):
    title = models.CharField(max_length=225)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.IntegerField()

