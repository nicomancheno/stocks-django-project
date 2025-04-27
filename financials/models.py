from django.db import models

class Company(models.Model):
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.symbol


class IncomeStatement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    fiscal_date_ending = models.DateField()
    
    total_revenue = models.FloatField(null=True, blank=True)
    cost_of_revenue = models.FloatField(null=True, blank=True)
    gross_profit = models.FloatField(null=True, blank=True)
    net_income = models.FloatField(null=True, blank=True)
    basic_average_shares = models.FloatField(null=True, blank=True)
    basic_eps = models.FloatField(null=True, blank=True)
    operating_expense = models.FloatField(null=True, blank=True)
    ebitda = models.FloatField(null=True, blank=True)
    ebit = models.FloatField(null=True, blank=True)
    operating_income = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('company', 'fiscal_date_ending')

    def __str__(self):
        return f'{self.company.name} Income Statement - {self.fiscal_date_ending}'
    
class BalanceSheet(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    fiscal_date_ending = models.DateField()

    # Selected important fields for the balance sheet
    total_assets = models.FloatField(null=True, blank=True)
    total_liabilities_net_minority_interest = models.FloatField(null=True, blank=True)
    total_equity_gross_minority_interest = models.FloatField(null=True, blank=True)
    net_tangible_assets = models.FloatField(null=True, blank=True)
    common_stock_equity = models.FloatField(null=True, blank=True)
    long_term_debt = models.FloatField(null=True, blank=True)
    working_capital = models.FloatField(null=True, blank=True)
    total_capitalization = models.FloatField(null=True, blank=True)
    cash_and_cash_equivalents = models.FloatField(null=True, blank=True)
    retained_earnings = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.company.name} Balance Sheet - {self.fiscal_date_ending}"

from django.db import models

class CashFlowStatement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    fiscal_date_ending = models.DateField()

    # The new fields you asked to add
    free_cash_flow = models.FloatField(null=True, blank=True)
    repayment_of_debt = models.FloatField(null=True, blank=True)
    issuance_of_debt = models.FloatField(null=True, blank=True)
    issuance_of_capital_stock = models.FloatField(null=True, blank=True)
    capital_expenditure = models.FloatField(null=True, blank=True)
    interest_paid_supplemental_data = models.FloatField(null=True, blank=True)
    income_tax_paid_supplemental_data = models.FloatField(null=True, blank=True)
    end_cash_position = models.FloatField(null=True, blank=True)
    beginning_cash_position = models.FloatField(null=True, blank=True)
    effect_of_exchange_rate_changes = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.company.name} - {self.fiscal_date_ending}'