from decimal import Decimal
from typing import Dict

from rest_framework import serializers

from tasks.models import Book, Purchase
from tasks.services import PurchaseGenerator


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "price")


class BookPurchaseSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Purchase
        fields = ("books", "total_cost")

    def get_total_cost(self, obj: Purchase) -> Decimal:
        return obj.operation.amount

    def create(self, validated_data: Dict) -> Purchase:
        books_ids = [book.id for book in validated_data.get("books")]
        purchase_generator = PurchaseGenerator(
            user=self.context["request"].user, books=books_ids
        )
        purchase = purchase_generator.make_purchase()
        return purchase
