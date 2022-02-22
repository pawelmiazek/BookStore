# Generated by Django 3.0.6 on 2022-02-22 13:49

from decimal import Decimal

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "current_balance",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=8
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="account",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Account",
                "verbose_name_plural": "Accounts",
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150, verbose_name="title")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="price"
                    ),
                ),
            ],
            options={
                "verbose_name": "Book",
                "verbose_name_plural": "Books",
            },
        ),
        migrations.CreateModel(
            name="Operation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("DEPOSIT", "deposit"), ("PURCHASE", "purchase")],
                        max_length=8,
                        verbose_name="type",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="amount"
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="operations",
                        to="tasks.Account",
                        verbose_name="account",
                    ),
                ),
            ],
            options={
                "verbose_name": "Operation",
                "verbose_name_plural": "Operations",
            },
        ),
        migrations.CreateModel(
            name="Purchase",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "books",
                    models.ManyToManyField(
                        related_name="purchases", to="tasks.Book", verbose_name="books"
                    ),
                ),
                (
                    "operation",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchase",
                        to="tasks.Operation",
                        verbose_name="operation",
                    ),
                ),
            ],
            options={
                "verbose_name": "Purchase",
                "verbose_name_plural": "Purchases",
            },
        ),
    ]
