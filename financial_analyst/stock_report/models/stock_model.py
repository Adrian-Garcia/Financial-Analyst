from django.db import models
from .fundamental_analysis_model import FundamentalAnalysis
from django.utils import timezone
from urllib.request import urlopen
import json
import certifi
import yfinance as yf

API_KEY = "58f91c97ad7ca8846322ee09d634a66c"


class Stock(models.Model):
    fundamental_analyses = models.ManyToManyField(FundamentalAnalysis)

    # Stock basic info
    ticker = models.CharField(max_length=15)
    name = models.CharField(max_length=30)
    last_update = models.DateTimeField(default=timezone.now)

    # Price
    stock_price = models.FloatField(default=0)
    stock_price_bid = models.FloatField(default=0)
    stock_price_ask = models.FloatField(default=0)

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

    # TODO: Calculate next 6 ratios

    # Five year ratios
    price_earnings_five_years = models.FloatField(default=0)
    price_to_sales_five_years = models.FloatField(default=0)
    price_to_book_five_years = models.FloatField(default=0)

    # Real ratios values
    real_price_earnings = models.FloatField(default=0)
    real_price_to_sales = models.FloatField(default=0)
    real_price_to_book = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.ticker}: {self.name}"

    def update_stock_ratios(self) -> bool:
        if (
            self.__financialmodelingprep_update_stock_ratios()
            and self.__yf_update_stock_ratios()
        ):
            self.save()
            return True

        return False

    def __financialmodelingprep_update_stock_ratios(self) -> bool:
        url = f"https://financialmodelingprep.com/api/v3/ratios/{self.ticker}?apikey={API_KEY}"
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        json_data = json.loads(data)

        if not json_data:
            return False

        latest_year = json_data[0]
        latest_year = {ratio: value or 0 for (ratio, value) in latest_year.items()}

        self.cash_ratio = latest_year["cashRatio"]
        self.inventory_turnover = latest_year["inventoryTurnover"]
        self.assets_turnover = latest_year["assetTurnover"]

        self.net_margin = latest_year["netProfitMargin"]
        self.days_inventory = latest_year["daysOfInventoryOutstanding"]

        self.price_earnings = latest_year["priceEarningsRatio"]
        self.price_cash_flow = latest_year["priceCashFlowRatio"]
        self.price_to_sales = latest_year["priceToSalesRatio"]

        return True

    def __yf_update_stock_ratios(self) -> bool:
        yf_stock_info = yf.Ticker(self.ticker).info

        if not yf_stock_info:
            return False

        self.name = yf_stock_info["shortName"]
        self.stock_price_ask = yf_stock_info["ask"]
        self.stock_price_bid = yf_stock_info["bid"]
        self.stock_price = (self.stock_price_bid + self.stock_price_ask) / 2

        self.current_ratio = yf_stock_info["currentRatio"]
        self.quick_ratio = yf_stock_info["quickRatio"]

        self.debt_equity = yf_stock_info["debtToEquity"]
        self.return_on_equity = yf_stock_info["returnOnEquity"]
        self.price_to_book = yf_stock_info["priceToBook"]

        return True
