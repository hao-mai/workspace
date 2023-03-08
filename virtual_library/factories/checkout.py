import factory
from virtual_library.models import Checkout
from virtual_library.factories.books import BookFactory
from virtual_library.factories.user import UserFactory
import datetime as dt

class CheckoutFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Checkout
    book = factory.SubFactory(BookFactory)
    borrower = factory.SubFactory(UserFactory)
    return_date = dt.date.today() + dt.timedelta(days=14)
