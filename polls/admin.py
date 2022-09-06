"""
Admin
"""
from django.contrib import admin
from .models import Item, Order, BillingAddress, Payment, Refund

class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'ordered', 'delivering', 'delivered', 'refunded', 'checkout_failure']
    list_filter = ['ordered', 'delivering', 'delivered', 'refunded', 'checkout_failure']
    search_fields = ['user__username', 'ref_code']


admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Refund)
# Register your models here.
