from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response

from CustomAssignment.api.filters import DateFilter
from CustomAssignment.api.serializers import ProductSerializer, OrderSerializer, StatsSerializer
from CustomAssignment.products.models import Product, Order


@api_view(['GET'])
def stats_list(request):
    date_start = request.GET.get('date_start', None)
    date_end = request.GET.get('date_end', None)
    metric = request.GET.get('metric', None)

    if not date_start or not date_end or not metric:
        return Response({'error': 'Please enter all of the input fields: [date_start, date_end, metric=price/count].'})

    if date_start:
        orders = Order.objects.all().filter(date__gte=date_start, date__lte=date_end).order_by('date')
    else:
        orders = Order.objects.all().order_by('date')
    used_months = {

    }

    stats = []
    for item in orders:
        month = item.date.month
        year = item.date.year
        if year not in used_months:
            used_months[year] = []
        if month not in used_months[year]:
            stats.append(item)
            used_months[year].append(month)

    for item in Order.objects.all():
        item.metric = metric
        item.save()

    serializer = StatsSerializer(stats, many=True)

    return Response(serializer.data)


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('pk')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = DateFilter


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


def index_view(request):
    return render(request, 'index.html', {})
