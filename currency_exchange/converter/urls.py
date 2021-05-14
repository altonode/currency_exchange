from django.urls import path, re_path

from .views import converter_view

app_name = "converter"

urlpatterns = [
    path("", view=converter_view, name="index"),
]
