from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField

SIZE_CHOICES = (
    ('XS', 'Extra Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
)

DESIGN_CHOICES = (
    ('TLS', 'Top left small'),
    ('TRS', 'Top right small'),
    ('CF', 'Centre front'),
    ('CB', 'Centre back'),
    ('FB', 'Front and back'),
)

COLOUR_CHOICES = (
    ('red', 'Red'),
    ('wht', 'White'),
    ('blk', 'Black'),
)

def validate_quantity(value):
    if value < 1:
        raise ValidationError(
        _('%(value)s is not a valid quantity.'),
        params={'value':value}
    )

class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.FloatField()
    title = models.CharField(max_length=100, default="New Item", unique=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=2)
    design = models.CharField(choices=DESIGN_CHOICES, max_length=3)
    colour = models.CharField(choices=COLOUR_CHOICES, max_length=3)
    
    quantity = models.IntegerField(default=1, validators=[validate_quantity])

    def __str__(self):
        return self.title
    
    def get_total_price(self):
        return self.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.user.get_username() + "'s order with " + str(self.quantity) + " shirts."

    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += (item.price * item.quantity)

        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username + "'s billing address."

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__():
        return user.username + "'s " + amount + " order."