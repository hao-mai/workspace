from virtual_library.factories import BookFactory, UserFactory
from rest_framework import status
from rest_framework.test import APITestCase
from virtual_library.models import Book, Genre
from django.urls import reverse
from virtual_library.serializers import BookSerializer



class VirtualLibraryTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.genre1 = Genre.objects.create(name='Science Fiction')
        cls.genre2 = Genre.objects.create(name='Action')
        cls.author1 = 'Author One'
        cls.author2 = 'Author Two'
        cls.book1 = BookFactory(title='Book One', author=cls.author1, genre=[cls.genre1])
        cls.book2 = BookFactory(title='Book Two', author=cls.author2, genre=[cls.genre2], available=False)
    
    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_list_books(self):

        # Test list view for authenticated admin user
        self.user = UserFactory(is_superuser=True)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('book-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Test list view for authenticated non-admin user
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('book-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        # Test list view for unauthenticated user
        self.client.logout()
        response = self.client.get(reverse('book-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_book(self):
        book = BookFactory()
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        book = Book.objects.get(id=self.book1.id)
        serializer = BookSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_available_books(self):
        url = reverse('book-available-books')
        response = self.client.get(url)
        available_books = Book.objects.filter(available=True)
        serializer = BookSerializer(available_books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_unavailable_book(self):
        url = reverse('book-detail', args=[self.book2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_book(self):

        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'summary': 'A summary of the new book',
            'author': self.author1,
            'genre': [self.genre1.id, self.genre2.id],
            'num_pages': 100,
        }
        response = self.client.post(url, data, format='json')
        book = Book.objects.get(title='New Book')
        serializer = BookSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_update_book(self):

        # create a book
        book = BookFactory()
        # prepare data for update
        updated_title = 'Updated Title'
        updated_author = 'Updated Author'
        updated_genre = [self.genre1, self.genre2]
        data = {
            'title': updated_title,
            'author': updated_author,
            'genre': [genre.id for genre in updated_genre],
            'available': True,  # set to False to make sure it updates correctly
        }
        # send update request
        response = self.client.patch(reverse('book-detail', args=[book.id]), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check that book was updated correctly
        book.refresh_from_db()
        self.assertEqual (book.title,updated_title)
        self.assertEqual(book.author,updated_author)
        self.assertEqual(set(book.genre.all()),set(updated_genre))
        self.assertTrue(book.available)




