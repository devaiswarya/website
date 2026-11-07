from django.urls import path
from .views import create_contact

urlpatterns = [
    path("contact/create/", create_contact),
]