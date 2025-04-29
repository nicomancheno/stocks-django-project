from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Company, IncomeStatement, BalanceSheet, CashFlowStatement
from datetime import date
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from django.core import serializers  # if not already imported
import json

# Make sure to use a valid API key for your application.
API_KEY = '9HYXP1EZDX7HU3IM'

def home(request):
    return render(request, 'home.html')


def fetch_or_update_financials(symbol):
    # Fetch the company object or create a new one
    company, created = Company.objects.get_or_create(symbol=symbol)

    # Fetch financial data from Yahoo Finance using yfinance
    stock = yf.Ticker(symbol)
    
    # Get the financials data
    income_statement = stock.financials.transpose()  # Transpose to make dates rows
    balance_sheet = stock.balance_sheet.transpose()  # Transpose to make dates rows
    cashflow_statement = stock.cashflow.transpose()  # Transpose to make dates rows

    

    # Parse and save the financial data
    for date, row in income_statement.iterrows():
        fiscal_date = date.date()  # This gets just the date part, no time
        IncomeStatement.objects.update_or_create(
            company=company,
            fiscal_date_ending=fiscal_date,
            defaults={
                'total_revenue': row.get('Total Revenue', 0),
                'cost_of_revenue': row.get('Cost Of Revenue', 0),
                'gross_profit': row.get('Gross Profit', 0),
                'net_income': row.get('Net Income', 0),
                'basic_average_shares': row.get('Basic Average Shares', 0),
                'basic_eps': row.get('Basic EPS', 0),
                'operating_expense': row.get('Operating Expense', 0),
                'ebitda': row.get('EBITDA', 0),
                'ebit': row.get('EBIT', 0),
                'operating_income': row.get('Operating Income', 0),
            }

        )

    for date, row in balance_sheet.iterrows():
        fiscal_date = date.date()  # Get only the date, no time
        BalanceSheet.objects.update_or_create(
            company=company,
            fiscal_date_ending=fiscal_date,
            defaults={
                'total_assets': row.get('Total Assets', 0),
                'total_liabilities_net_minority_interest': row.get('Total Liabilities Net Minority Interest', 0),
                'total_equity_gross_minority_interest': row.get('Total Equity Gross Minority Interest', 0),
                'net_tangible_assets': row.get('Net Tangible Assets', 0),
                'common_stock_equity': row.get('Common Stock Equity', 0),
                'long_term_debt': row.get('Long Term Debt', 0),
                'working_capital': row.get('Working Capital', 0),
                'total_capitalization': row.get('Total Capitalization', 0),
                'cash_and_cash_equivalents': row.get('Cash And Cash Equivalents', 0),
                'retained_earnings': row.get('Retained Earnings', 0),
            }
        )

    for date, row in cashflow_statement.iterrows():
        # Convert the date from Timestamp to string (only date part)
        fiscal_date = date.date()  # This gets just the date part, no time
        CashFlowStatement.objects.update_or_create(
            company=company,
            fiscal_date_ending=fiscal_date,
            defaults={
                'free_cash_flow': row.get('Free Cash Flow', 0),
                'repayment_of_debt': row.get('Repayment Of Debt', 0),
                'issuance_of_debt': row.get('Issuance Of Debt', 0),
                'issuance_of_capital_stock': row.get('Issuance Of Capital Stock', 0),
                'capital_expenditure': row.get('Capital Expenditure', 0),
                'interest_paid_supplemental_data': row.get('Interest Paid Supplemental Data', 0),
                'income_tax_paid_supplemental_data': row.get('Income Tax Paid Supplemental Data', 0),
                'end_cash_position': row.get('End Cash Position', 0),
                'beginning_cash_position': row.get('Beginning Cash Position', 0),
                'effect_of_exchange_rate_changes': row.get('Effect Of Exchange Rate Changes', 0),
            }

        )

    return company


def financials_view(request):
    symbol = request.GET.get('symbol', 'AAPL')  # Default to 'AAPL' if no symbol is provided

    # Fetch or update financial data for the given symbol
    company = fetch_or_update_financials(symbol)

    # Define start date (2021-01-01)
    start_date = date(2021, 1, 1)

    # Retrieve the financial reports for the company from 2021 onwards
    income_reports = IncomeStatement.objects.filter(
        company=company, fiscal_date_ending__gte=start_date
    ).order_by('-fiscal_date_ending')

    balance_reports = BalanceSheet.objects.filter(
        company=company, fiscal_date_ending__gte=start_date
    ).order_by('-fiscal_date_ending')

    cashflow_reports = CashFlowStatement.objects.filter(
        company=company, fiscal_date_ending__gte=start_date
    ).order_by('-fiscal_date_ending')

    # Format date fields and convert QuerySet to a list of dictionaries
    def format_report_dates(report):
        # Convert date fields to string in YYYY-MM-DD format
        report['fiscal_date_ending'] = report['fiscal_date_ending'].strftime('%Y-%m-%d')
        return report

    income_reports_list = list(income_reports.values())
    income_reports_list = [format_report_dates(report) for report in income_reports_list]

    cashflow_reports_list = list(cashflow_reports.values())
    cashflow_reports_list = [format_report_dates(report) for report in cashflow_reports_list]

    # Serialize the lists to JSON
    income_reports_json = json.dumps(income_reports_list)
    cashflow_reports_json = json.dumps(cashflow_reports_list)

    return render(request, 'financials.html', {
        'symbol': symbol,
        'income_reports': income_reports,
        'balance_reports': balance_reports,
        'cashflow_reports': cashflow_reports,
        'income_reports_json': income_reports_json,
        'cashflow_reports_json': cashflow_reports_json,
    })



def calculate_growth(new, old):
    if old and old != 0:
        return ((float(new) - float(old)) / abs(float(old))) * 100
    return None

