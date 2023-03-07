import factory
from virtual_library.models import Book

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=4)
    author = factory.Faker('name')
    description = factory.Faker('paragraph')
    num_pages = factory.Faker('random_int', min=50, max=500)
    available = True
    quantity = 1

    @factory.post_generation
    def genre(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            if isinstance(extracted, list):
                # If `extracted` is a list, add all the genres to the book
                for genre in extracted:
                    self.genre.add(genre)
            else:
                # If `extracted` is a single object, add it to the book
                self.genre.add(extracted)
