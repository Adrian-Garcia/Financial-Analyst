from django.db import models
from django.utils import timezone


class FundamentalAnalysis(models.Model):

    # Fundamental Analysis basic information
    name = models.CharField(max_length=30)
    industry = models.CharField(max_length=30)
    last_update = models.DateTimeField(default=timezone.now)

    # Averages of the ratios of the stocks
    avg_price = models.FloatField(default=0)
    avg_current_ratio = models.FloatField(default=0)
    avg_quick_ratio = models.FloatField(default=0)
    avg_cash_ratio = models.FloatField(default=0)
    avg_debt_equity = models.FloatField(default=0)
    avg_inventory_turnover = models.FloatField(default=0)
    avg_days_inventory = models.FloatField(default=0)
    avg_assets_turnover = models.FloatField(default=0)
    avg_return_on_equity = models.FloatField(default=0)
    avg_net_margin = models.FloatField(default=0)
    avg_price_earnings = models.FloatField(default=0)
    avg_price_cash_flow = models.FloatField(default=0)
    avg_price_to_sales = models.FloatField(default=0)
    avg_price_to_book = models.FloatField(default=0)

    # Id of the best stock according to model
    best_stock_id = models.IntegerField(default=0)
    best_stock_value = models.FloatField(default=0)

    # Calculations to determine actual value
    historical = models.FloatField(default=0)
    intrinsic_by_industry = models.FloatField(default=0)
    final_value = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.name

    def __restart_averages(self) -> None:
        self.avg_price = 0
        self.avg_current_ratio = 0
        self.avg_quick_ratio = 0
        self.avg_cash_ratio = 0
        self.avg_debt_equity = 0
        self.avg_inventory_turnover = 0
        self.avg_days_inventory = 0
        self.avg_assets_turnover = 0
        self.avg_return_on_equity = 0
        self.avg_net_margin = 0
        self.avg_price_earnings = 0
        self.avg_price_cash_flow = 0
        self.avg_price_to_sales = 0
        self.avg_price_to_book = 0

    # TODO: Solve when Dayss Inventory & InventoryTurnover are 0
    def calculate_avg_ratios(self) -> None:
        stocks = self.stock_set.all()
        if not stocks:
            return

        self.__restart_averages()

        for stock in stocks:
            self.avg_price += stock.price
            self.avg_current_ratio += stock.current_ratio
            self.avg_quick_ratio += stock.quick_ratio
            self.avg_cash_ratio += stock.cash_ratio
            self.avg_debt_equity += stock.debt_equity
            self.avg_inventory_turnover += stock.inventory_turnover
            self.avg_days_inventory += stock.days_inventory
            self.avg_assets_turnover += stock.assets_turnover
            self.avg_return_on_equity += stock.return_on_equity
            self.avg_net_margin += stock.net_margin
            self.avg_price_earnings += stock.price_earnings
            self.avg_price_cash_flow += stock.price_cash_flow
            self.avg_price_to_sales += stock.price_to_sales
            self.avg_price_to_book += stock.price_to_book

        num_stock = len(stocks)

        self.avg_price /= num_stock
        self.avg_current_ratio /= num_stock
        self.avg_quick_ratio /= num_stock
        self.avg_cash_ratio /= num_stock
        self.avg_debt_equity /= num_stock
        self.avg_inventory_turnover /= num_stock
        self.avg_days_inventory /= num_stock
        self.avg_assets_turnover /= num_stock
        self.avg_return_on_equity /= num_stock
        self.avg_net_margin /= num_stock
        self.avg_price_earnings /= num_stock
        self.avg_price_cash_flow /= num_stock
        self.avg_price_to_sales /= num_stock
        self.avg_price_to_book /= num_stock

        self.save()

    def calculate_best_stock(self) -> None:
        stocks = self.stock_set.all()
        best_percentage = float("-inf")
        best_stock_value = 0
        best_stock_id = None

        if not stocks:
            return

        for stock in stocks:
            stock_real_value = stock.get_real_stock_value(self)
            current_percentage = stock_real_value / stock.price

            if current_percentage > best_percentage:
                best_percentage = current_percentage
                best_stock_id = stock.id

        self.best_stock_id = best_stock_id
        self.best_stock_value = best_stock_value
