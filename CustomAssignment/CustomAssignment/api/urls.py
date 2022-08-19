from django.urls import path

from CustomAssignment.api.views import OrderViewset, ProductViewset, stats_list
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'orders', OrderViewset, basename='orders',
)
router.register(
    r'products', ProductViewset, basename='products',
)


urlpatterns = [
    path('stats/', stats_list, name='stats'),
] + router.urls
