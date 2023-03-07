from rest_framework import viewsets
from virtual_library.models import Book
from virtual_library.serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as django_filters
from rest_framework.decorators import action
from rest_framework.response import Response

class BookFilterSet(django_filters.FilterSet):
    genre = django_filters.Filter(field_name='genres__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'available']

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to view available books.
    """
    queryset = Book.objects.filter(available=True)
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookFilterSet
    ordering = ['title']
    ordering_fields = ['title', 'author', 'genres', 'year']
    search_fields = ['title', 'author', 'genres', 'year']

    @action(detail=False)
    def available_books(self, request):
        available_books = Book.objects.filter(available=True)
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)
