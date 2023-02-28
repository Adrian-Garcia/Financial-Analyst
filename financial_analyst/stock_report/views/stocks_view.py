from django.urls import reverse
from typing import List
from stock_report.models.stock_model import Stock
from stock_report.models.fundamental_analysis_model import FundamentalAnalysis
from stock_report.error_handlers.stock_error_handler import (
    get_single_stock_errors,
    get_stock_errors,
)
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
            continue

        stocks.append(ticker)

    return stocks


def stock_detail(request: WSGIRequest, stock_id: int) -> HttpResponse:
    stock = get_object_or_404(Stock, pk=stock_id)
    return render(
        request,
        "stock_report/stocks/detail.html",
        {"stock": stock},
    )


def new_stock(request: WSGIRequest) -> HttpResponse:
    stock = Stock()
    return render(
        request, "stock_report/stocks/new.html", {"stock": stock, "errors": ""}
    )


def create_stock(request: WSGIRequest) -> HttpResponseRedirect:
    stock = Stock.generate_stock(request)
    errors = get_single_stock_errors(stock)

    if errors:
        return render(
            request,
            "stock_report/stocks/new.html",
            {"stock": stock, "errors": errors},
        )

    stock.calculate_real_values()
    stock.save()
    return HttpResponseRedirect(reverse("stock_reports:stock_detail", args=(stock.id,)))


def add_stock(
    request: WSGIRequest, fundamental_analysis_id: int
) -> HttpResponseRedirect:
    fundamental_analysis = get_object_or_404(
        FundamentalAnalysis, pk=fundamental_analysis_id
    )

    tickers = request.POST["tickers"]
    stocks = get_stocks(tickers.upper())
    errors = get_stock_errors(fundamental_analysis, stocks)

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

    fundamental_analysis.calculate_avg_ratios()
    fundamental_analysis.calculate_best_stock()

    return HttpResponseRedirect(
        reverse("stock_reports:detail", args=(fundamental_analysis.id,))
    )
