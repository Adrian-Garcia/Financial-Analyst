from typing import List
from stock_report.models.fundamental_analysis_model import FundamentalAnalysis
from stock_report.models.stock_model import Stock


def not_found_tickers(stocks: List[str]) -> List[str]:
    errors = []

    for stock in stocks:
        if type(stock) != Stock:
            errors.append(f"El ticker {stock} no pudo ser encontrado")

    return errors


def get_stock_errors(
    fundamental_analysis: FundamentalAnalysis, stocks: List[str]
) -> List[str]:
    errors = not_found_tickers(stocks)

    for stock in stocks:
        if stock in fundamental_analysis.stock_set.all():
            errors.append(f"{stock} ya se encuentra dentro del analisis fundamental")

    return errors


# TODO: Add more validations for correct data
def get_single_stock_errors(stock: Stock) -> List[str]:
    errors = []

    existing_stock = Stock.objects.filter(ticker=stock.ticker)

    if existing_stock:
        errors.append(f"Ya existe una accion con el ticker {stock.ticker}")

    if not stock.name:
        errors.append("La acción no tiene nombre")

    if not stock.ticker:
        errors.append("La acción no tiene ticker")

    if not stock.price:
        errors.append("La acción no tiene precio")

    if not stock.price_earnings:
        errors.append("Price Earnings debe tener valor")

    if not stock.price_to_sales:
        errors.append("Price to Sales debe tener valor")

    if not stock.price_to_book:
        errors.append("Price to Book debe tener valor")

    return errors
