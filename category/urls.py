from rest_framework.urls import path
from .views import create_category, upload_file,get_categories

urlpatterns=[
    path("create_category/", create_category, name="create_category"),
    path("upload_file/", upload_file, name="upload_file"),
    path('getall/',get_categories,name="get_categories")
]