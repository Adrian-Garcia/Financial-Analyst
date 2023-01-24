from django.urls import path
from . import views

app_name = "stock_reports"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:fundamental_analysis_id>/", views.detail, name="detail"),
]
