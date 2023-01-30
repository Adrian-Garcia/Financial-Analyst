from typing import List
from stock_report.error_handler.stock_error_handler import get_stock_errors
from stock_report.models.fundamental_analysis_model import FundamentalAnalysis
from stock_report.models.stock_model import Stock


def get_fundamental_analysis_errors(
    fundamental_analysis: FundamentalAnalysis, stocks: List[str]
) -> List[str]:
    errors = []
    if not fundamental_analysis.name:
        errors.append("Analisis Fundamental debe tener nombre")

    errors += get_stock_errors(fundamental_analysis, stocks)
    return errors
