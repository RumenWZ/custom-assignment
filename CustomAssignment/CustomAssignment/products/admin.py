from django.contrib import admin

from CustomAssignment.products.models import Product, Order

admin.site.register(Product)
admin.site.register(Order)
