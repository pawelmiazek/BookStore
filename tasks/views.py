from django.db.models import Sum
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from tasks.models import Book, Operation
from tasks.serializers import BookPurchaseSerializer, BookSerializer


class BookViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "buy":
            return BookPurchaseSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "buy":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(methods=["post"], detail=False)
    def buy(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        purchase_amount = Book.objects.filter(
            id__in=request.data.get("books")
        ).aggregate(purchase=Sum("price"))["purchase"]
        operation = Operation.objects.create(
            type=Operation.TypeChoices.PURCHASE,
            account=request.user.account,
            amount=purchase_amount,
        )
        serializer.save(operation_id=operation.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
