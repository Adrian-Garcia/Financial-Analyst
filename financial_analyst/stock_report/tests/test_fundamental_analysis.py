from typing import List
from stock_report.tests.test_stock import create_stock
from django.test import TestCase
from django.urls import reverse
from stock_report.models.modelFundamentalAnalysis import FundamentalAnalysis


def create_fundamental_analysis(name: str) -> FundamentalAnalysis:
    return FundamentalAnalysis.objects.create(name=name)


class FundamentalAnalysisDetailViewTest(TestCase):
    def test_existing_fundamental_analysis_with_stocks(self) -> None:
        fundamental_analysis = create_fundamental_analysis("FANG")
        google_stock = create_stock("Google", "GOOGL", [fundamental_analysis])
        amazon_stock = create_stock("Amazon", "AMZN", [fundamental_analysis])

        response = self.client.get(
            reverse("stock_reports:detail", args=(fundamental_analysis.id,))
        )

        self.assertContains(response, fundamental_analysis)
        self.assertContains(response, google_stock.name)
        self.assertContains(response, amazon_stock.name)

    def test_existing_fundamental_analysis_without_stocks(self) -> None:
        fundamental_analysis = create_fundamental_analysis("FANG")

        response = self.client.get(
            reverse("stock_reports:detail", args=(fundamental_analysis.id,))
        )

        self.assertContains(response, fundamental_analysis)
        self.assertContains(
            response, "El análisis fundamental no tiene acciones para analizar"
        )

    def test_nonexistent_fundamental_analysis(self) -> None:
        response = self.client.get(reverse("stock_reports:detail", args=(0,)))

        self.assertEqual(response.status_code, 404)
