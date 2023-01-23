from django.db import models


class FundamentalAnalysis(models.Model):
    name = models.CharField(max_length=30)
    industry = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Stock(models.Model):
    fundamental_analysis = models.ForeignKey(
        FundamentalAnalysis, on_delete=models.CASCADE
    )

    ticker = models.CharField(max_length=15)
    name = models.CharField(max_length=30)

    # Ratios
    current_ratio = models.FloatField()
    quick_ratio = models.FloatField()
    cash_ratio = models.FloatField()
    debt_equity = models.FloatField()
    inventory_turnover = models.FloatField()
    days_inventory = models.FloatField()
    assets_turnover = models.FloatField()
    roe = models.FloatField()
    net_margin = models.FloatField()
    per = models.FloatField()
    pcf = models.FloatField()
    ps = models.FloatField()
    pbv = models.FloatField()

    # Five year ratios
    per_five_years = models.FloatField()
    ps_five_years = models.FloatField()
    pbv_five_years = models.FloatField()

    def __str__(self):
        return self.name
