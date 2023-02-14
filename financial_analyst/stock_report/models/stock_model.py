from django.db import models
from .fundamental_analysis_model import FundamentalAnalysis
from django.utils import timezone
from urllib.request import urlopen
import json
import certifi
import yfinance as yf
from statistics import mean

# TODO: Add this to .env file
API_KEY = "58f91c97ad7ca8846322ee09d634a66c"


class Stock(models.Model):
    fundamental_analyses = models.ManyToManyField(FundamentalAnalysis)

    # Stock basic info
    ticker = models.CharField(max_length=15)
    name = models.CharField(max_length=30)
    last_update = models.DateTimeField(default=timezone.now)

    # Price
    price = models.FloatField(default=0)
    price_bid = models.FloatField(default=0)
    price_ask = models.FloatField(default=0)

    # Ratios
    current_ratio = models.FloatField(default=0)
    quick_ratio = models.FloatField(default=0)
    cash_ratio = models.FloatField(default=0)
    debt_equity = models.FloatField(default=0)
    inventory_turnover = models.FloatField(default=0)
    days_inventory = models.FloatField(default=0)
    assets_turnover = models.FloatField(default=0)
    return_on_equity = models.FloatField(default=0)
    net_margin = models.FloatField(default=0)
    price_earnings = models.FloatField(default=0)
    price_cash_flow = models.FloatField(default=0)
    price_to_sales = models.FloatField(default=0)
    price_to_book = models.FloatField(default=0)

    # Five year ratios
    price_earnings_five_years = models.FloatField(default=0)
    price_to_sales_five_years = models.FloatField(default=0)
    price_to_book_five_years = models.FloatField(default=0)

    # TODO: Verify that this variables are correctly named
    # Real ratios values
    real_price_earnings = models.FloatField(default=0)
    real_price_to_sales = models.FloatField(default=0)
    real_price_to_book = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.ticker}: {self.name}"

    def update_stock_ratios(self) -> bool:
        if not self.__yf_update_stock_ratios():
            return False

        if not self.__financialmodelingprep_update_stock_ratios():
            return False

        self.save()
        return True

    def valuate_stock(self, fundamental_analysis) -> float:
        historical = (self.real_price_to_sales + self.real_price_to_book) / 2

        per_current_value = (fundamental_analysis.avg_price_earnings * self.price) / 2
        pcf_current_value = (fundamental_analysis.avg_price_cash_flow * self.price) / 2
        ps_current_value = (fundamental_analysis.avg_price_to_sales * self.price) / 2
        pbv_current_value = (fundamental_analysis.avg_price_to_book * self.price) / 2

        intrinsic_by_industry = mean(
            [per_current_value, pcf_current_value, ps_current_value, pbv_current_value]
        )

        final_value = (historical + intrinsic_by_industry) / 2

        # TODO: Create a class called valuation to store this information
        return {
            "final_value": final_value,
            "current_percentage": final_value / self.price,
            "intrinsic_by_industry": intrinsic_by_industry,
            "historical": historical,
            "per_current_value": per_current_value,
            "pcf_current_value": pcf_current_value,
            "ps_current_value": ps_current_value,
            "pbv_current_value": pbv_current_value,
        }

    def __set_five_year_ratios(self, ratios) -> None:
        if len(ratios) >= 5:
            ratios = ratios[:5]

        price_earnings_five_years = []
        price_to_sales_five_years = []
        price_to_book_five_years = []

        for stock in ratios:
            price_earnings_five_years.append(stock["priceEarningsRatio"])
            price_to_sales_five_years.append(stock["priceToSalesRatio"])
            price_to_book_five_years.append(stock["priceToBookRatio"])

        self.price_earnings_five_years = mean(price_earnings_five_years)
        self.price_to_sales_five_years = mean(price_to_sales_five_years)
        self.price_to_book_five_years = mean(price_to_book_five_years)

    def __financialmodelingprep_update_stock_ratios(self) -> bool:
        url = f"https://financialmodelingprep.com/api/v3/ratios/{self.ticker}?apikey={API_KEY}"
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        ratios = json.loads(data)

        if not ratios:
            return False

        latest_year = ratios[0]
        latest_year = {ratio: value or 0 for (ratio, value) in latest_year.items()}

        self.cash_ratio = latest_year["cashRatio"]
        self.inventory_turnover = latest_year["inventoryTurnover"]
        self.assets_turnover = latest_year["assetTurnover"]

        self.net_margin = latest_year["netProfitMargin"]
        self.days_inventory = latest_year["daysOfInventoryOutstanding"]

        self.price_earnings = latest_year["priceEarningsRatio"]
        self.price_cash_flow = latest_year["priceCashFlowRatio"]
        self.price_to_sales = latest_year["priceToSalesRatio"]

        self.__set_five_year_ratios(ratios)

        self.real_price_earnings = (
            self.price * self.price_earnings_five_years / self.price_earnings
        )

        self.real_price_to_sales = (
            self.price * self.price_to_sales_five_years / self.price_to_sales
        )

        self.real_price_to_book = (
            self.price * self.price_to_book_five_years / self.price_to_book
        )

        return True

    def __yf_update_stock_ratios(self) -> bool:
        try:
            ratios = yf.Ticker(self.ticker).info
        except:
            return False

        if not ratios:
            return False

        self.name = ratios["shortName"]
        self.price_ask = ratios["ask"]
        self.price_bid = ratios["bid"]
        self.price = (self.price_bid + self.price_ask) / 2

        self.current_ratio = ratios["currentRatio"]
        self.quick_ratio = ratios["quickRatio"]

        self.debt_equity = ratios["debtToEquity"]
        self.return_on_equity = ratios["returnOnEquity"]
        self.price_to_book = ratios["priceToBook"]

        return True
