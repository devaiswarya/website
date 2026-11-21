
from django.urls import path
from .views import login_api,register_api

urlpatterns = [
    path('login/', login_api, name='login'),
    path('register/', register_api, name='register'),
]
