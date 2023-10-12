from django.contrib import admin
from .models import Order, OrderItems

admin.site.register(OrderItems)
admin.site.register(Order)
