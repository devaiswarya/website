from django.urls import path
from .views import create_deal, get_today_deals, update_deal

urlpatterns = [

    path(
        "deals/create/",
        create_deal,
        name="create_deal"
    ),
    path(
        "deals/today/",
        get_today_deals,
        name="get_today_deals"
    ),

    path(
        "deals/update/<str:deal_id>/",
        update_deal,
        name="update_deal"
    ),
]