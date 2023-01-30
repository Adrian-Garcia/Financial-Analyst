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
