from typing import List
from stock_report.models.fundamental_analysis_model import FundamentalAnalysis
from stock_report.models.stock_model import Stock


def get_fundamental_analysis_errors(
    fundamental_analysis: FundamentalAnalysis, stocks: List[str]
) -> List[str]:
    errors = []
    if not fundamental_analysis.name:
        errors.append("Analisis Fundamental debe tener nombre")

    for stock in stocks:
        if type(stock) != Stock:
            errors.append(f"El ticker {stock} no pudo ser encontrado")

    return errors