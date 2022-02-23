from decimal import Decimal

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tasks.factories import AccountFactory, BookFactory, UserFactory
from tasks.models import Account, Operation


@pytest.fixture
def factory_account(db):
    account = AccountFactory(current_balance=Decimal(2000))
    return account


@pytest.fixture
def factory_books(db):
    books = BookFactory.create_batch(4)
    return books


@pytest.mark.django_db
def test_book_list_allow_any():
    client = APIClient()
    url = "/books/"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_book_buy_allow_any(factory_books):
    client = APIClient()
    url = "/books/buy/"
    data = {"books": [book.id for book in factory_books]}

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_book_buy_success(factory_account, factory_books):
    client = APIClient()
    client.force_authenticate(user=factory_account.user)
    purchase = sum([book.price for book in factory_books])
    url = "/books/buy/"
    data = {"books": [book.id for book in factory_books]}

    response = client.post(url, data=data)
    account = Account.objects.get(id=factory_account.id)

    assert response.status_code == status.HTTP_201_CREATED
    assert (
        factory_account.current_balance - account.current_balance
    ) == purchase
    assert Operation.objects.filter(account=account, amount=purchase).exists()


@pytest.mark.django_db
def test_book_buy_without_account(factory_books):
    client = APIClient()
    user = UserFactory()
    client.force_authenticate(user=user)
    url = "/books/buy/"
    data = {"books": [book.id for book in factory_books]}

    response = client.post(url, data=data)
    error = "Current User need account for making purchases."

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == error


@pytest.mark.django_db
def test_book_buy_without_enough_balance(factory_books):
    client = APIClient()
    account = AccountFactory(current_balance=Decimal(50))
    client.force_authenticate(user=account.user)
    url = "/books/buy/"
    data = {"books": [book.id for book in factory_books]}

    response = client.post(url, data=data)
    error = "Purchase amount cannot be higher than account's current balance."

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == error


@pytest.mark.django_db
def test_book_buy_balance_equal_to_purchase(factory_books):
    client = APIClient()
    purchase = sum([book.price for book in factory_books])
    account = AccountFactory(current_balance=purchase)
    client.force_authenticate(user=account.user)
    url = "/books/buy/"
    data = {"books": [book.id for book in factory_books]}

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Account.objects.get(id=account.id).current_balance == 0
