import factory
from django.contrib.auth import get_user_model
from faker import Factory

from tasks.models import Account, Book

User = get_user_model()
faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.LazyAttribute(lambda _: faker.word())
    last_name = factory.LazyAttribute(lambda _: faker.word())
    username = factory.LazyAttribute(lambda _: faker.word())
    email = factory.LazyAttribute(
        lambda u: "{}.{}@example.com".format(u.first_name, u.last_name).lower()
    )


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    user = factory.SubFactory(UserFactory)


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.LazyAttribute(lambda _: faker.word())
    price = factory.Sequence(lambda n: "%d" % (n + 50))
