from rest_framework import serializers
from virtual_library.models import Checkout

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ['id', 'book', 'borrower', 'checkout_date', 'return_date']
        read_only_fields = ['id', 'checkout_date', 'return_date']
