"""
Admin
"""
from django.contrib import admin
from .models import Item, Order, BillingAddress, Payment

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(BillingAddress)
admin.site.register(Payment)
# Register your models here.
