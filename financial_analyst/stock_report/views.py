from typing import List
from django.urls import reverse
from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

from stock_report.models.modelFundamentalAnalysis import FundamentalAnalysis
from stock_report.models.modelStock import Stock


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


def stock_detail(request: WSGIRequest, stock_id: int) -> HttpResponse:
    stock = get_object_or_404(Stock, pk=stock_id)
    return render(
        request,
        "stock_report/stocks/detail.html",
        {"stock": stock},
    )


def new_fundamental_analysis(request: WSGIRequest) -> HttpResponse:
    fundamental_analysis = FundamentalAnalysis()
    return render(
        request,
        "stock_report/create.html",
        {"fundamental_analysis": fundamental_analysis, "tickers": ""},
    )


# Move function away from this file
def get_stocks(tickers: str) -> List[Stock]:
    stocks = []

    for ticker in tickers.split():
        stock = Stock.objects.filter(ticker=ticker)

        if stock:
            stocks.append(stock.first())
            continue

        stock = Stock(ticker=ticker)
        if stock.update_stock_ratios():
            stocks.append(stock)
            stock.save()
            continue

        stocks.append(ticker)

    return stocks


# Move function away from this file
def get_errors(
    fundamental_analysis: FundamentalAnalysis, stocks: List[str]
) -> List[str]:
    errors = []
    if not fundamental_analysis.name:
        errors.append("Analisis Fundamental debe tener nombre")

    for stock in stocks:
        if type(stock) != Stock:
            errors.append(f"El ticker {stock} no pudo ser encontrado")

    return errors


def create_fundamental_analysis(
    request: WSGIRequest,
) -> HttpResponseRedirect:
    fundamental_analysis = FundamentalAnalysis()
    fundamental_analysis.name = request.POST["name"]
    fundamental_analysis.industry = request.POST["industry"]
    tickers = request.POST["tickers"]

    stocks = get_stocks(tickers.upper())
    errors = get_errors(fundamental_analysis, stocks)

    if not errors:
        fundamental_analysis.save()
        for stock in stocks:
            stock.fundamental_analyses.add(fundamental_analysis)
            stock.save()

        return HttpResponseRedirect(
            reverse("stock_reports:detail", args=(fundamental_analysis.id,))
        )

    return render(
        request,
        "stock_report/create.html",
        {
            "fundamental_analysis": fundamental_analysis,
            "tickers": tickers,
            "errors": errors,
        },
    )
