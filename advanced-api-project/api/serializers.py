from .models import Author, Book
from rest_framework import serializers
from datetime import date

# The relationship between Author and Book is handled using a nested serializer,
# allowing BookSerializer to include detailed Author information (via AuthorSerializer)
# rather than just an ID. This makes it possible to read and write data for both models
# in a single request while preserving their foreign key relationship.


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
            current_year = date.today().year
            if value > current_year:
                raise serializers.ValidationError("Publication year cannot be in the future.")
            return value


    

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['id','name','books']



