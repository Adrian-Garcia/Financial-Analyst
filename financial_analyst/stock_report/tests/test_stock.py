from django.test import TestCase
from django.urls import reverse
from stock_report.models import Stock


def createStock(name: str, ticker: str) -> Stock:
    return Stock.objects.create(name=name, ticker=ticker)


class StockDetailViewTest(TestCase):
    def test_nonexistent_stock(self):
        response = self.client.get(reverse("stock_reports:stock_detail", args=(0,)))
        self.assertEqual(response.status_code, 404)

    def test_existing_stock(self):
        stock = createStock("Google", "GOOGL")
        response = self.client.get(
            reverse("stock_reports:stock_detail", args=(stock.id,))
        )

        self.assertContains(response, stock.name)
        self.assertContains(response, stock.ticker)
