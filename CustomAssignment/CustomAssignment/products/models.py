import datetime

from django.core.validators import MinLengthValidator
from django.db import models


class Product(models.Model):
    PRODUCT_TITLE_MAX_LEN = 60
    PRODUCT_TITLE_MIN_LEN = 2

    PRICE_MAX_DIGITS = 6

    title = models.CharField(
        max_length=PRODUCT_TITLE_MAX_LEN,
        blank=False,
        null=False,
        validators=(
            MinLengthValidator(PRODUCT_TITLE_MIN_LEN),
        )
    )

    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=2,
        blank=False,
        null=False,
        default=99.99,
    )

    def __str__(self):
        return f'{self.title}'


class Order(models.Model):
    date = models.DateField(
        default=datetime.date.today,
        blank=False,
        null=False,
    )

    products = models.ManyToManyField(
        Product,
        related_name='orders',
    )

    # I understand this is a pretty bad way to solve the problem, I tried 3 other simpler methods
    # but there was always something which prevented it from working.
    metric = models.CharField(
        max_length=5,
        default='price',
        editable=False,
    )

    def __str__(self):
        return f'Order number: {self.pk}, {self.date}'
