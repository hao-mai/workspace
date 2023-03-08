
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from virtual_library.models import Checkout
from virtual_library.factories import CheckoutFactory, BookFactory, UserFactory
import json
from virtual_library.serializers import CheckoutSerializer

class CheckoutViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.book = BookFactory(title='Book One', author='Author One', available=True)
        cls.checkout = CheckoutFactory.create(book=cls.book, borrower=cls.user)

        cls.valid_payload = {
            'book_id': cls.book.id,
        }
    
    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_create_checkout(self):
        b = BookFactory(title='Book One', author='Author One', available=True, quantity=2)

        response = self.client.post(reverse('checkout-list'), data=json.dumps({
            'book_id': b.id,
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        b.refresh_from_db()
        self.assertEqual(Checkout.objects.count(), 2)

        self.assertEqual(b.quantity, 1)
        self.assertFalse(b.available)

    def test_create_checkout_with_invalid_book_id(self):
        invalid_payload = {
            'book_id': 999,
        }
        response = self.client.post(reverse('checkout-list'), data=json.dumps(invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_checkout_when_book_is_not_available(self):
        self.book.available = False
        self.book.save()
        response = self.client.post(reverse('checkout-list'), data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_early(self):
        response = self.client.post(reverse('checkout-return-early', args=[self.checkout.id]), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book.refresh_from_db()

        self.assertTrue(self.book.available)
        self.assertEqual(self.book.quantity, 1)
        self.assertEqual(Checkout.objects.count(), 0)

    def test_list_checkouts(self):
        response = self.client.get(reverse('checkout-list'))
        checkouts = Checkout.objects.filter(borrower=self.user)
        serializer = CheckoutSerializer(checkouts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)