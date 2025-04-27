from django.db import models

class Company(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.symbol

class IncomeStatement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    fiscal_date_ending = models.DateField()
    total_revenue = models.BigIntegerField(null=True, blank=True)
    net_income = models.BigIntegerField(null=True, blank=True)
    reported_eps = models.FloatField(null=True, blank=True)
    common_shares_outstanding = models.BigIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('company', 'fiscal_date_ending')

class BalanceSheet(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    fiscal_date_ending = models.DateField()
    total_assets = models.BigIntegerField(null=True, blank=True)
    total_liabilities = models.BigIntegerField(null=True, blank=True)
    total_shareholder_equity = models.BigIntegerField(null=True, blank=True)
    cash_and_cash_equivalents = models.BigIntegerField(null=True, blank=True)
    short_term_debt = models.BigIntegerField(null=True, blank=True)
    long_term_debt = models.BigIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('company', 'fiscal_date_ending')

class CashFlowStatement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    fiscal_date_ending = models.DateField()
    operating_cashflow = models.BigIntegerField(null=True, blank=True)
    free_cashflow = models.BigIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('company', 'fiscal_date_ending')
