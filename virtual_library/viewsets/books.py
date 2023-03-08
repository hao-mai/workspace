from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from virtual_library.models import Book
from virtual_library.serializers import BookSerializer
from django_filters import rest_framework as django_filters
from rest_framework.decorators import action
from rest_framework.response import Response


class BookFilterSet(django_filters.FilterSet):
    genre = django_filters.Filter(field_name='genres__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'available']

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view available books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilterSet
    ordering = ['title']
    ordering_fields = ['title', 'author', 'genre', 'year']
    search_fields = ['title', 'author', 'genre', 'year']

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        elif self.request.user.is_authenticated and self.request.user.is_staff:
            return [IsAdminUser()]
        else:
            return []

    def get_queryset(self):
        if self.request.user.is_superuser:
            # Return all books for admin users
            return Book.objects.all()
        elif self.request.user.is_authenticated and self.request.user.is_staff:
            # Only return available books for non-admin users
            return Book.objects.filter(available=True)
        else:
            # Non-admin users can only view available books
            return Book.objects.filter(available=True)



    @action(detail=False)
    def available_books(self, request):
        available_books = Book.objects.filter(available=True)
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)
