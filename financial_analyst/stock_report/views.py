from typing import List
from django.urls import reverse
from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import FundamentalAnalysis, Stock


class IndexView(generic.ListView):
    template_name = "stock_report/index.html"
    context_object_name = "fundamental_analysis_list"

    def get_queryset(self):
        return FundamentalAnalysis.objects.all()


def detail(request, fundamental_analysis_id):
    fundamental_analysis = get_object_or_404(
        FundamentalAnalysis, pk=fundamental_analysis_id
    )
    return render(
        request,
        "stock_report/detail.html",
        {"fundamental_analysis": fundamental_analysis},
    )


def new_fundamental_analysis(request):
    fundamental_analysis = FundamentalAnalysis()
    return render(
        request,
        "stock_report/create.html",
        {"fundamental_analysis": fundamental_analysis},
    )

# Move function away from this file
def get_stocks(tickers: str) -> List[Stock]:
    res_stocks = []

    for ticker in tickers.split():
        stock = Stock.objects.filter(ticker=ticker)

        if stock:
            res_stocks.append(stock.first())
            continue

        stock = Stock(ticker=ticker)
        if stock.update_stock_ratios():
            res_stocks.append(stock)
            stock.save()
            continue

        res_stocks.append(ticker)

    return res_stocks

# Move function away from this file
def get_errors(fundamental_analysis: FundamentalAnalysis, stocks: List[Stock]) -> List[str]:
    errors = []
    if not fundamental_analysis.name:
        errors.append("Analisis Fundamental debe tener nombre")
    
    for stock in stocks:
        if type(stock) != Stock:
            errors.append(f"El ticker {stock} no pudo ser encontrado")
    
    return errors

def create_fundamental_analysis(request):
    fundamental_analysis = FundamentalAnalysis()
    fundamental_analysis.name = request.POST["name"]
    fundamental_analysis.industry = request.POST["industry"]

    stocks = get_stocks(request.POST["tickers"].upper())
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
            "errors": errors,
        },
    )
