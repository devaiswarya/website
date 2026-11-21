from rest_framework.urls import path
from .views import add_to_cart,get_cart

urlpatterns=[
    path('add/',add_to_cart,name='add_to_cart'),
    path('get/',get_cart,name='get_cart'),
]