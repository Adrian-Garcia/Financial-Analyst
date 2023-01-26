from django.urls import path
from stock_report.views.viewStocks import stock_detail
from stock_report.views.viewFundamentalAnalysis import (
    IndexView,
    detail,
    new_fundamental_analysis,
    create_fundamental_analysis,
)


app_name = "stock_reports"
urlpatterns = [
    # ex: /stock_report/
    path("", IndexView.as_view(), name="index"),
    # ex: /stock_report/1/
    path("<int:fundamental_analysis_id>/", detail, name="detail"),
    # ex: /stock_report/new/
    path("new/", new_fundamental_analysis, name="new"),
    # ex: POST /stock_report/create/
    path("create/", create_fundamental_analysis, name="create"),
    # ex: /stock_report/stock/1/
    path("stock/<int:stock_id>/", stock_detail, name="stock_detail"),
]
