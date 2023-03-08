import factory
from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    is_staff = False
    is_superuser = False
    is_active = True

    @factory.post_generation
    def authenticated(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.is_authenticated = True
            self.save()
