from typing import List
from stock_report.tests.test_stock import create_stock
from django.test import TestCase
from django.urls import reverse
from stock_report.models.fundamental_analysis_model import FundamentalAnalysis


class FundamentalAnalysisDetailViewTest(TestCase):
    def test_existing_fundamental_analysis_with_stocks(self) -> None:
        fundamental_analysis = FundamentalAnalysis.objects.create(name="FANG")
        google_stock = create_stock("GOOGL", "Google", [fundamental_analysis])
        amazon_stock = create_stock("AMZN", "Amazon", [fundamental_analysis])

        response = self.client.get(
            reverse("stock_reports:detail", args=(fundamental_analysis.id,))
        )

        self.assertContains(response, fundamental_analysis)
        self.assertContains(response, google_stock)
        self.assertContains(response, amazon_stock)

    def test_existing_fundamental_analysis_without_stocks(self) -> None:
        fundamental_analysis = FundamentalAnalysis.objects.create(name="FANG")

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

    def test_delete_stock_from_fundamental_analysis(self):
        fundamental_analysis = FundamentalAnalysis.objects.create(name="FANG")
        google_stock = create_stock("GOOGL", "Google", [fundamental_analysis])
        amazon_stock = create_stock("AMZN", "Amazon", [fundamental_analysis])

        response_delete = self.client.get(
            reverse(
                "stock_reports:delete_stock_from_fundamental_analysis",
                args=(
                    fundamental_analysis.id,
                    google_stock.id,
                ),
            )
        )
        self.assertEqual(response_delete.status_code, 302)

        response_get = self.client.get(
            reverse("stock_reports:detail", args=(fundamental_analysis.id,))
        )

        self.assertNotContains(response_get, google_stock)
        self.assertContains(response_get, amazon_stock)
