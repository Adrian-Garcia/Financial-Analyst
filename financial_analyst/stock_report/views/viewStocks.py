from typing import List
from stock_report.models.modelStock import Stock
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


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


def stock_detail(request: WSGIRequest, stock_id: int) -> HttpResponse:
    stock = get_object_or_404(Stock, pk=stock_id)
    return render(
        request,
        "stock_report/stocks/detail.html",
        {"stock": stock},
    )
