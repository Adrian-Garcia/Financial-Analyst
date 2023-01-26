from django.contrib import admin
from stock_report.models.modelStock import Stock
from stock_report.models.modelFundamentalAnalysis import FundamentalAnalysis

admin.site.register(FundamentalAnalysis)
admin.site.register(Stock)
