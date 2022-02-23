from decimal import Decimal
from typing import List, Optional

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from tasks.models import Account, Book, Operation, Purchase

User = get_user_model()


class PurchaseGenerator:
    def __init__(self, user: User, books: Optional[List[int]] = None) -> None:
        self.purchase_amount: Decimal = (
            Book.objects.select_for_update()
            .filter(id__in=books)
            .aggregate(purchase=Sum("price"))["purchase"]
            or Decimal("0.00")
        )
        self.user: User = user
        self.books: List[int] = books

    def make_purchase(self) -> Operation:
        self.validate_purchase_amount()
        self.deduct_purchase_from_account()

        operation = Operation.objects.create(
            type=Operation.TypeChoices.PURCHASE,
            account=self.user.account,
            amount=self.purchase_amount,
        )
        purchase = Purchase.objects.create(operation=operation)
        purchase.books.set(self.books)
        return purchase

    def validate_purchase_amount(
        self,
    ) -> Optional[serializers.ValidationError]:
        if not hasattr(self.user, "account"):
            raise serializers.ValidationError(
                _("Current User need account for making purchases.")
            )

        if (
            self.user.account.current_balance - self.purchase_amount
        ) < Decimal(0):
            raise serializers.ValidationError(
                _(
                    "Purchase amount cannot be higher than account's"
                    + " current balance."
                )
            )

    def deduct_purchase_from_account(self) -> None:
        deducted_value = (
            self.user.account.current_balance - self.purchase_amount
        )
        Account.objects.select_for_update().filter(
            id=self.user.account.id
        ).update(current_balance=deducted_value)
