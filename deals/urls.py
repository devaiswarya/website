from django.urls import path
from . import views

urlpatterns = [

    path(
        "deals/create/",
        views.create_deal,
        name="create_deal"
    ),
    path(
        "deals/today/",
        views.get_today_deals,
        name="get_today_deals"
    ),

    path(
        "deals/update/<str:deal_id>/",
        views.update_deal,
        name="update_deal"
    ),
]