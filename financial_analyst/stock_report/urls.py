from django.urls import path
from . import views

app_name = "stock_reports"
urlpatterns = [
    path("", views.index, name="index"),
]
