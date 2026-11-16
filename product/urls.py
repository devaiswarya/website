from rest_framework.urls import path
from .views import create_product,get_new_arrivals,get_products,global_search

urlpatterns=[
    path("create_product/", create_product, name="create_product"),  
    path("get_new_arrivals/", get_new_arrivals, name="get_new_arrivals"),
    path("products/", get_products, name="get_products"),
    path('global/',global_search,name="global_search"),
]