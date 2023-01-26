from django.urls import path
from . import views

app_name = "stock_reports"
urlpatterns = [
    # ex: /stock_report/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /stock_report/1/
    path("<int:fundamental_analysis_id>/", views.detail, name="detail"),
    # ex: /stock_report/new/
    path("new/", views.new_fundamental_analysis, name="new"),
    # ex: POST /stock_report/create/
    path("create/", views.create_fundamental_analysis, name="create"),
    # ex: /stock_report/stock/1/
    path("stock/<int:stock_id>/", views.stock_detail, name="stock_detail"),
]
