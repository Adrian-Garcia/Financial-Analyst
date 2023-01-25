from django.utils import timezone
from django.db import models
from urllib.request import urlopen
import json
import certifi

API_KEY = "58f91c97ad7ca8846322ee09d634a66c"

class FundamentalAnalysis(models.Model):
    name = models.CharField(max_length=30)
    industry = models.CharField(max_length=30)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Stock(models.Model):
    fundamental_analysis = models.ForeignKey(
        FundamentalAnalysis, on_delete=models.CASCADE
    )

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
    roe = models.FloatField(default=0)
    net_margin = models.FloatField(default=0)
    per = models.FloatField(default=0)
    pcf = models.FloatField(default=0)
    ps = models.FloatField(default=0)
    pbv = models.FloatField(default=0)

    # Five year ratios
    per_five_years = models.FloatField(default=0)
    ps_five_years = models.FloatField(default=0)
    pbv_five_years = models.FloatField(default=0)

    def __str__(self):
        return f"{self.ticker}: {self.name}"

    def update_stock_ratios(self):
        url = (f"https://financialmodelingprep.com/api/v3/ratios/{self.ticker}?apikey={API_KEY}")
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        json_data = json.loads(data)
        latest_year = json_data[0]

        self.stock_price = None
        self.current_ratio = latest_year["currentRatio"]
        self.quick_ratio = latest_year["quickRatio"]
        self.cash_ratio = latest_year["cashRatio"]
        self.debt_equity = latest_year["debtEquityRatio"]
        self.inventory_turnover = latest_year["inventoryTurnover"]
        self.days_inventory = latest_year["daysOfInventoryOutstanding"] # Not sure about this
        self.assets_turnover = latest_year["assetTurnover"]
        # self.roe
        self.net_margin = latest_year["netProfitMargin"] # Not sure about this
        # self.per
        # self.pcf
        # self.ps
        # self.pbv

        
