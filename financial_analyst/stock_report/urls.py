from django.urls import path
from . import views

app_name = "stock_reports"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:fundamental_analysis_id>/", views.detail, name="detail"),
    path("new/", views.new_fundamental_analysis, name="new"),
    path("create/", views.create_fundamental_analysis, name="create"),
]
