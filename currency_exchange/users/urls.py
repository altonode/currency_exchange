from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from currency_exchange.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    register_profile,
    profile_update_view,
    profile,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("~register-profile/", view=register_profile, name="register_profile"),
    path("~profile/<str:username>/", view=profile, name="profile"),
    path("~update-profile/<str:username>/", view=profile_update_view, name="update_profile"),
    path("<str:username>/", view=user_detail_view, name="detail"),

]
