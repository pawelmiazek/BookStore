from decimal import Decimal

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tasks.factories import AccountFactory, BookFactory


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
def test_book_buy_is_authenticated(factory_account, factory_books):
    client = APIClient()
    client.force_authenticate(user=factory_account.user)
    url = "/books/buy/"
    data = {"books": [book.id for book in factory_books]}

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
