from rest_framework import serializers
from virtual_library.models import Book

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'num_pages', 'available', 'quantity']
