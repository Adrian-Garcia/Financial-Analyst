from django.urls import path
from stock_report.views.stocks_view import stock_detail, add_stock, new_stock, create_stock
from stock_report.views.fundamental_analysis_view import (
    IndexView,
    detail,
    new_fundamental_analysis,
    create_fundamental_analysis,
    delete_stock_from_fundamental_analysis,
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
    # ex: /stock_report/stock/new/
    path("stock/new/", new_stock, name="new_stock"),
    # ex: POST /stock_report/stock/create/
    path("stock/create/", create_stock, name="create_stock"),
    # ex: /stock_report/stock/1/
    path("stock/<int:stock_id>/", stock_detail, name="stock_detail"),
    # ex: POST /stock_report/stock/1
    path("<int:fundamental_analysis_id>", add_stock, name="add_stock"),
    # ex: /stock_report/delete_stock_from_fundamental_analysis/1/1
    path(
        "<int:fundamental_analysis_id>/<int:stock_id>",
        delete_stock_from_fundamental_analysis,
        name="delete_stock_from_fundamental_analysis",
    ),
]
