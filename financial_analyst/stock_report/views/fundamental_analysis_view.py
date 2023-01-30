from django.urls import reverse
from django.views import generic
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from stock_report.error_handler.fundamental_analysis_error_handler import (
    get_fundamental_analysis_errors,
)
from stock_report.models.stock_model import Stock
from stock_report.models.fundamental_analysis_model import FundamentalAnalysis
from stock_report.views.stocks_view import get_stocks
from typing import List


class IndexView(generic.ListView):
    template_name = "stock_report/index.html"
    context_object_name = "fundamental_analysis_list"

    def get_queryset(self) -> List[FundamentalAnalysis]:
        return FundamentalAnalysis.objects.all()


def detail(request: WSGIRequest, fundamental_analysis_id: int) -> HttpResponse:
    fundamental_analysis = get_object_or_404(
        FundamentalAnalysis, pk=fundamental_analysis_id
    )
    return render(
        request,
        "stock_report/detail.html",
        {"fundamental_analysis": fundamental_analysis},
    )


def new_fundamental_analysis(request: WSGIRequest) -> HttpResponse:
    fundamental_analysis = FundamentalAnalysis()
    return render(
        request,
        "stock_report/new.html",
        {"fundamental_analysis": fundamental_analysis, "tickers": ""},
    )


def create_fundamental_analysis(
    request: WSGIRequest,
) -> HttpResponseRedirect:
    fundamental_analysis = FundamentalAnalysis()
    fundamental_analysis.name = request.POST["name"]
    fundamental_analysis.industry = request.POST["industry"]
    tickers = request.POST["tickers"]

    stocks = get_stocks(tickers.upper())
    errors = get_fundamental_analysis_errors(fundamental_analysis, stocks)

    if errors:
        return render(
            request,
            "stock_report/new.html",
            {
                "fundamental_analysis": fundamental_analysis,
                "tickers": tickers,
                "errors": errors,
            },
        )

    fundamental_analysis.save()
    for stock in stocks:
        stock.fundamental_analyses.add(fundamental_analysis)
        stock.save()

    fundamental_analysis.calculate_avg_ratios()

    return HttpResponseRedirect(
        reverse("stock_reports:detail", args=(fundamental_analysis.id,))
    )