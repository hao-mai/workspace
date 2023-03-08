from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from virtual_library.models import Checkout, Book
from virtual_library.serializers import CheckoutSerializer
from rest_framework.decorators import action
from datetime import date, timedelta


class CheckoutViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows users to checkout books.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CheckoutSerializer
    queryset = Checkout.objects.all()

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book_id', None)
        user_id = request.user.id

        # Check if book is available
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not book.available:
            return Response({'error': 'Book is not available.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create checkout
        checkout = Checkout(book=book, borrower_id=user_id, return_date=date.today() + timedelta(days=14))
        checkout.save()

        # Return checkout details
        serializer = CheckoutSerializer(checkout)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def return_early(self, request, pk=None):
        checkout = self.get_object()
        book = checkout.book
        checkout_obj = Checkout.objects.get(book=checkout.book, borrower=request.user)

        # Handle "return book early" functionality here
        if not book.available:
            book.available = True
            book.quantity += 1
            book.save()  # save the changes to the book object
        checkout_obj.delete()
        return Response({'message': 'Book returned early'})


    def list(self, request):
        queryset = Checkout.objects.filter(borrower=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
