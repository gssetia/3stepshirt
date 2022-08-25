from django.db import models
from django.conf import settings
from django.urls import reverse

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

COLOUR_CHOICES = {
    ('red', 'Red'),
    ('wht', 'White'),
    ('blk', 'Black'),
}

class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.FloatField()
    title = models.CharField(max_length=100, default="New Item")
    size = models.CharField(choices=SIZE_CHOICES, max_length=2)
    design = models.CharField(choices=DESIGN_CHOICES, max_length=3)
    colour = models.CharField(choices=COLOUR_CHOICES, max_length=3)
    
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def get_remove_from_cart_url(self):
        print("tfd")
        return reverse("add-to-cart", kwargs={
            'value':self.title
        })


# class OrderItem(models.Model):
    
    
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
    

#     def __str__(self):
#         return f"{self.quantity} of {self.item.title}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)


    def __str__(self):
        #return self.title
        return "test"
