from django.urls import path
from .views import home, about, design, add_to_cart, cart

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('cart/', cart, name='cart'),
    path('design/', design, name='design'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
]