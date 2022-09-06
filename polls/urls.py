from django.urls import path
from .views import home, about, design, cart, checkout, payment, profile

urlpatterns = [
    path('', home, name='home'),
    # path('about/', about, name='about'),
    path('cart/', cart, name='cart'),
    path('design/', design, name='design'),
    path('checkout/', checkout, name='checkout'),
    path('payment/<payment_option>', payment, name='payment'),
    path('profile/', profile, name='profile'),
    #path('add-to-cart/', add_to_cart, name='add-to-cart'),
    #path('remove-from-cart/<value>/', remove_from_cart, name='remove-from-cart'),
]