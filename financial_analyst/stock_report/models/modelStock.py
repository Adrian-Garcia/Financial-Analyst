from django.db import models
from .modelFundamentalAnalysis import FundamentalAnalysis
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

    # Ratios
    stock_price = models.FloatField(default=0)
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
    per_five_years = models.FloatField(default=0)
    ps_five_years = models.FloatField(default=0)
    pbv_five_years = models.FloatField(default=0)

    def __str__(self):
        return f"{self.ticker}: {self.name}"

    def update_stock_ratios(self) -> bool:
        url = f"https://financialmodelingprep.com/api/v3/ratios/{self.ticker}?apikey={API_KEY}"
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        json_data = json.loads(data)

        if not json_data:
            return False

        latest_year = json_data[0]
        latest_year = {ratio: value or 0 for (ratio, value) in latest_year.items()}

        self.stock_price = 0.0
        self.current_ratio = latest_year["currentRatio"]
        self.quick_ratio = latest_year["quickRatio"]
        self.cash_ratio = latest_year["cashRatio"]
        self.debt_equity = latest_year["debtEquityRatio"]
        self.inventory_turnover = latest_year["inventoryTurnover"]
        self.assets_turnover = latest_year["assetTurnover"]

        self.net_margin = latest_year["netProfitMargin"]
        self.days_inventory = latest_year["daysOfInventoryOutstanding"]

        self.return_on_equity = latest_year["returnOnEquity"]
        self.price_earnings = latest_year["priceEarningsRatio"]
        self.price_cash_flow = latest_year["priceCashFlowRatio"]
        self.price_to_sales = latest_year["priceToSalesRatio"]
        self.price_to_book = latest_year["priceToBookRatio"]

        return True
