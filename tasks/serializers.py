from decimal import Decimal

from rest_framework import serializers

from tasks.models import Book, Purchase


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "price")


class BookPurchaseSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Purchase
        fields = ("books", "amount")

    def get_amount(self, obj: Purchase) -> Decimal:
        return obj.operation.amount
