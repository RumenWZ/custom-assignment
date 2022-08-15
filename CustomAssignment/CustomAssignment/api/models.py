from django.core.validators import MinLengthValidator
from django.db import models


class Product(models.Model):
    PRODUCT_TITLE_MAX_LEN = 60
    PRODUCT_TITLE_MIN_LEN = 2

    PRICE_MAX_DIGITS = 6

    title = models.CharField(
        max_length=PRODUCT_TITLE_MAX_LEN,
        validators=(
            MinLengthValidator(PRODUCT_TITLE_MIN_LEN),
        )
    )

    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=2,
    )


class Order(models.Model):
    date = models.DateField(
        auto_now_add=True,
    )
