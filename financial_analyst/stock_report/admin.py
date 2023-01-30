from django.contrib import admin
from stock_report.models.stock_model import Stock
from stock_report.models.fundamental_analysis_model import FundamentalAnalysis

admin.site.register(FundamentalAnalysis)
admin.site.register(Stock)
