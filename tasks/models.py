from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Account(models.Model):
    """
    Account model holds current balance of every user.
    """

    user = models.OneToOneField(
        User, verbose_name="user", related_name="account", on_delete=models.CASCADE
    )
    current_balance = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal("0.00")
    )

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self) -> str:
        return self.user.username


class Operation(models.Model):
    """
    Each change (deposit, purchase, etc..) of Account's balance should be reflected
    in the Operation model for auditing purposes.
    """

    class TypeChoices(models.TextChoices):
        DEPOSIT = "DEPOSIT", _("deposit")
        PURCHASE = "PURCHASE", _("purchase")

    type = models.CharField(
        verbose_name="type", max_length=8, choices=TypeChoices.choices
    )
    account = models.ForeignKey(
        Account,
        verbose_name="account",
        related_name="operations",
        on_delete=models.PROTECT,
    )
    amount = models.DecimalField(verbose_name="amount", max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "Operation"
        verbose_name_plural = "Operations"

    def __str__(self) -> str:
        return f"{self.account}: {self.get_type_display()}"


class Book(models.Model):
    """
    Model stores a title of the book and its price.
    """

    title = models.CharField(verbose_name="title", max_length=150)
    price = models.DecimalField(verbose_name="price", max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self) -> str:
        return self.title


class Purchase(models.Model):
    """
    Model stores data about purchases.
    """

    books = models.ManyToManyField(Book, verbose_name="books", related_name="purchases")
    operation = models.OneToOneField(
        Operation,
        verbose_name="operation",
        related_name="purchase",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"

    def __str__(self) -> str:
        return self.amount
