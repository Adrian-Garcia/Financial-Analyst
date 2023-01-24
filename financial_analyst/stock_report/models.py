from django.utils import timezone
from django.db import models


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
