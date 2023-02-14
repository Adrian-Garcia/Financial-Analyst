from django.test import TestCase
from django.urls import reverse
from stock_report.models.stock_model import Stock
from stock_report.models.fundamental_analysis_model import FundamentalAnalysis
import random


def create_stock(
    ticker: str, name: str = None, fundamental_analyses: FundamentalAnalysis = None
) -> Stock:
    # TODO: Implement a way to populate stock data more accurately
    random_price = random.uniform(1, 100)

    stock = Stock.objects.create(
        name=name,
        ticker=ticker,
        price=random_price,
        price_bid=random_price * 0.98,
        price_ask=random_price * 1.02,
        current_ratio=random.uniform(1, 3),
        quick_ratio=random.uniform(1, 3),
        cash_ratio=random.uniform(1, 3),
        debt_equity=random.uniform(1, 3),
        inventory_turnover=random.uniform(0, 150),
        days_inventory=random.uniform(0, 50),
        assets_turnover=random.uniform(0, 2),
        return_on_equity=random.uniform(0, 2),
        net_margin=random.uniform(0, 1),
        price_earnings=random.uniform(10, 100),
        price_cash_flow=random.uniform(10, 100),
        price_to_sales=random.uniform(0, 20),
        price_to_book=random.uniform(0, 20),
    )

    if fundamental_analyses:
        stock.fundamental_analyses.set(fundamental_analyses)

    return stock


class StockDetailViewTest(TestCase):
    def test_nonexistent_stock(self) -> None:
        response = self.client.get(reverse("stock_reports:stock_detail", args=(0,)))
        self.assertEqual(response.status_code, 404)

    def test_existing_stock(self) -> None:
        stock = create_stock("Google", "GOOGL")
        response = self.client.get(
            reverse("stock_reports:stock_detail", args=(stock.id,))
        )

        self.assertContains(response, stock)
