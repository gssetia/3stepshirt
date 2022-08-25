from django.urls import path
from .views import home, about, design, cart

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('cart/', cart, name='cart'),
    path('design/', design, name='design'),
    #path('add-to-cart/', add_to_cart, name='add-to-cart'),
    #path('remove-from-cart/<value>/', remove_from_cart, name='remove-from-cart'),
]