from django_filters import rest_framework as filters, DateTimeFilter
from django.db import models
from django import forms
from rest_framework.fields import CharField

from CustomAssignment.products.models import Order


class DateFilter(filters.FilterSet):
    contains_product = filters.CharFilter(
        field_name='products__title',
        lookup_expr='icontains',
        label='Also contains product')
    date_start = DateTimeFilter(
        field_name='date',
        lookup_expr='gte',
        label='Date start')
    date_end = DateTimeFilter(
        field_name='date',
        lookup_expr='lte',
        label='Date end'
    )

    class Meta:
        model = Order
        fields = (
            'contains_product',
            'date_start',
            'date_end',
        )
