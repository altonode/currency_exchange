from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from currency_exchange.transfer.views import (
    wallet_view,
    account_update_view,
    money_transfer_view,
)

app_name = "transfer"

urlpatterns = [
    path("~wallet/<str:username>/", view=wallet_view, name="wallet"),
    path("~update/<str:username>/", view=account_update_view, name="update"),
    path("~transfer/<uuid:account_uuid>", view=money_transfer_view, name="transfer")
]
