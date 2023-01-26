from django.test import TestCase
from django.urls import reverse
from stock_report.models import Stock, FundamentalAnalysis


def create_stock(
    name: str, ticker: str, fundamental_analyses: FundamentalAnalysis = None
) -> Stock:
    stock = Stock.objects.create(name=name, ticker=ticker)

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
