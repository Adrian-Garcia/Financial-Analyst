from django.urls import reverse
from typing import List
from stock_report.models.modelStock import Stock
from stock_report.models.modelFundamentalAnalysis import FundamentalAnalysis
from django.http import HttpResponseRedirect, HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, get_object_or_404


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


# TODO: Move function away from this file
def get_errors(
    fundamental_analysis: FundamentalAnalysis, stocks: List[str]
) -> List[str]:
    errors = []
    if not fundamental_analysis.name:
        errors.append("Analisis Fundamental debe tener nombre")

    for stock in stocks:
        if type(stock) != Stock:
            errors.append(f"El ticker {stock} no pudo ser encontrado")

        elif stock in fundamental_analysis.stock_set.all():
            errors.append(f"{stock} ya se encuentra dentro del analisis fundamental")

    return errors


def stock_detail(request: WSGIRequest, stock_id: int) -> HttpResponse:
    stock = get_object_or_404(Stock, pk=stock_id)
    return render(
        request,
        "stock_report/stocks/detail.html",
        {"stock": stock},
    )


def add_stock(
    request: WSGIRequest, fundamental_analysis_id: int
) -> HttpResponseRedirect:
    fundamental_analysis = get_object_or_404(
        FundamentalAnalysis, pk=fundamental_analysis_id
    )

    tickers = request.POST["tickers"]
    stocks = get_stocks(tickers.upper())
    # TODO: This should not work like this
    errors = get_errors(fundamental_analysis, stocks)

    if errors:

        return render(
            request,
            "stock_report/detail.html",
            {
                "fundamental_analysis": fundamental_analysis,
                "tickers": tickers,
                "errors": errors,
            },
        )

    for stock in stocks:
        stock.fundamental_analyses.add(fundamental_analysis)
        stock.save()

    return HttpResponseRedirect(
        reverse("stock_reports:detail", args=(fundamental_analysis.id,))
    )
