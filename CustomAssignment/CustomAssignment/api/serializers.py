from django.db.models import Sum, F
from django.db.models.functions import ExtractMonth
from rest_enumfield import EnumField
from rest_framework import serializers
from rest_framework.fields import FloatField
import enum

from CustomAssignment.api.helpers import months_of_the_year
from CustomAssignment.products.models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'date', 'products', ]
        depth = 1

    def create(self, validated_data):
        products = validated_data.pop('products', [])
        prdcts = []
        for product in products:
            obj = Product.objects.get(title=product['title'])
            prdcts.append(str(obj.pk))
        order = Order.objects.create(**validated_data)
        order.products.set(prdcts)
        return order

    def update(self, instance, validated_data):
        products = validated_data.pop('products', [])
        prdcts = []
        for product in products:
            obj = Product.objects.get(title=product['title'])
            prdcts.append(str(obj.pk))
        instance.products.set(prdcts)
        return instance


class StatsSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField('_get_month_and_year')
    value = serializers.SerializerMethodField('_get_value')

    def _get_value(self, order_object):
        values = Order.objects.filter(date__month=order_object.date.month, date__year=order_object.date.year)
        for item in values:
            if item.metric == 'count':
                orders_count = 0
                for value in values:
                    order_products_count = len(value.products.all())
                    orders_count += order_products_count
                return f'{orders_count}'
            elif item.metric == 'price':
                sum_of_the_month = 0
                for value in values:
                    summed_value = sum([a.price for a in value.products.all()])
                    sum_of_the_month += summed_value
                return f'{sum_of_the_month:.2f}'
            else:
                return f'Invalid Metric'

    def _get_month_and_year(self, order_object):
        month = months_of_the_year[order_object.date.month] + f' {str(order_object.date.year)}'
        return month

    class Meta:
        model = Order
        fields = ('month', 'value',)
