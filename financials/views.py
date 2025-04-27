from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Company, IncomeStatement, BalanceSheet, CashFlowStatement
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf

# Make sure to use a valid API key for your application.
API_KEY = '9HYXP1EZDX7HU3IM'

def home(request):
    return render(request, 'home.html')

def fetch_or_update_financials(symbol):
    company, created = Company.objects.get_or_create(symbol=symbol)

    # Fetch financials using Yahoo Finance scraping
    financials_df = fetch_yahoo_financials(symbol)

    # If no financial data is found, return the company object
    if financials_df is None:
        print(f"No financial data found for {symbol}.")
        return company

    # Process the financials data and save it to the database
    for index, row in financials_df.iterrows():
        fiscal_date = datetime.strptime(row['Date'], '%Y-%m-%d').date()

        # Ensure data is not missing or `None`
        IncomeStatement.objects.update_or_create(
            company=company,
            fiscal_date_ending=fiscal_date,
            defaults={
                'total_revenue': row.get('Total Revenue', 0),
                'net_income': row.get('Net Income', 0),
                'reported_eps': row.get('Earnings Per Share', 0),
                'common_shares_outstanding': row.get('Shares Outstanding', 0),
            }
        )

        BalanceSheet.objects.update_or_create(
            company=company,
            fiscal_date_ending=fiscal_date,
            defaults={
                'total_assets': row.get('Total Assets', 0),
                'total_liabilities': row.get('Total Liabilities', 0),
                'total_shareholder_equity': row.get('Total Shareholder Equity', 0),
                'cash_and_cash_equivalents': row.get('Cash and Cash Equivalents', 0),
                'short_term_debt': row.get('Short Term Debt', 0),
                'long_term_debt': row.get('Long Term Debt', 0),
            }
        )

        CashFlowStatement.objects.update_or_create(
            company=company,
            fiscal_date_ending=fiscal_date,
            defaults={
                'operating_cashflow': row.get('Operating Cash Flow', 0),
                'free_cashflow': row.get('Free Cash Flow', 0),
            }
        )

    return company

def fetch_yahoo_financials(symbol):
    # Fetch financial data from Yahoo Finance using the yfinance library
    stock = yf.Ticker(symbol)
    
    # Fetch the financials (Income statement, Balance sheet, Cash flow)
    financials = stock.financials.T  # Transpose to match your expected structure
    balance_sheet = stock.balance_sheet.T
    cashflow = stock.cashflow.T

    # Convert to DataFrame for easier handling
    financials_df = financials.reset_index()
    balance_sheet_df = balance_sheet.reset_index()
    cashflow_df = cashflow.reset_index()

    # Clean up headers (strip any leading/trailing spaces)
    financials_df.columns = financials_df.columns.str.strip()
    balance_sheet_df.columns = balance_sheet_df.columns.str.strip()
    cashflow_df.columns = cashflow_df.columns.str.strip()

    return financials_df, balance_sheet_df, cashflow_df

def fetch_or_update_financials(symbol):
    company, created = Company.objects.get_or_create(symbol=symbol)

    # Fetch financials using the yfinance API
    financials_df, balance_sheet_df, cashflow_df = fetch_yahoo_financials(symbol)

    # Process the financials data and save it to the database
    for _, row in financials_df.iterrows():
        fiscal_date = datetime.strptime(row['Date'], '%Y-%m-%d').date()

        IncomeStatement.objects.update_or_create(
            company=company,
            fiscal_date_ending=fiscal_date,
            defaults={
                'total_revenue': row.get('Total Revenue', 0),
                'net_income': row.get('Net Income', 0),
                'reported_eps': row.get('Earnings Per Share', 0),
                'common_shares_outstanding': row.get('Shares Outstanding', 0),
            }
        )

    for _, row in balance_sheet_df.iterrows():
        fiscal_date = datetime.strptime(row['Date'], '%Y-%m-%d').date()

        BalanceSheet.objects.update_or_create(
            company=company,
            fiscal_date_ending=fiscal_date,
            defaults={
                'total_assets': row.get('Total Assets', 0),
                'total_liabilities': row.get('Total Liabilities', 0),
                'total_shareholder_equity': row.get('Total Shareholder Equity', 0),
                'cash_and_cash_equivalents': row.get('Cash and Cash Equivalents', 0),
                'short_term_debt': row.get('Short Term Debt', 0),
                'long_term_debt': row.get('Long Term Debt', 0),
            }
        )

    for _, row in cashflow_df.iterrows():
        fiscal_date = datetime.strptime(row['Date'], '%Y-%m-%d').date()

        CashFlowStatement.objects.update_or_create(
            company=company,
            fiscal_date_ending=fiscal_date,
            defaults={
                'operating_cashflow': row.get('Operating Cash Flow', 0),
                'free_cashflow': row.get('Free Cash Flow', 0),
            }
        )

    return company

def calculate_growth(new, old):
    if old and old != 0:
        return ((float(new) - float(old)) / abs(float(old))) * 100
    return None

def financials_view(request):
    symbol = request.GET.get('symbol', 'AAPL')  # default is AAPL

    company = fetch_or_update_financials(symbol)

    # If no financial data was found, return an error or message
    if company is None:
        return render(request, 'financials.html', {'error': f"No financial data available for {symbol}"})

    income_reports = list(IncomeStatement.objects.filter(company=company).order_by('-fiscal_date_ending'))
    balance_reports = list(BalanceSheet.objects.filter(company=company).order_by('-fiscal_date_ending'))
    cashflow_reports = list(CashFlowStatement.objects.filter(company=company).order_by('-fiscal_date_ending'))

    revenue_growth = None
    earnings_growth = None
    shares_change = None
    free_cashflow_growth = None
    roic_list = []
    pe_ratios = []

    if len(income_reports) >= 5 and len(balance_reports) >= 5:
        # Revenue & Net Income Growth
        revenue_growth = calculate_growth(income_reports[0].total_revenue, income_reports[4].total_revenue)
        earnings_growth = calculate_growth(income_reports[0].net_income, income_reports[4].net_income)

        # Shares Outstanding Change
        shares_change = calculate_growth(income_reports[0].common_shares_outstanding, income_reports[4].common_shares_outstanding)

        # Free Cashflow Growth
        free_cashflow_growth = calculate_growth(cashflow_reports[0].operating_cashflow, cashflow_reports[4].operating_cashflow)

        # ROIC Calculation
        for income, balance in zip(income_reports[:5], balance_reports[:5]):
            if balance and income:
                nopat = float(income.net_income or 0) * 0.79  # assuming 21% tax
                invested_capital = (float(balance.total_liabilities or 0) + float(balance.total_shareholder_equity or 0)) - float(balance.cash_and_cash_equivalents or 0)
                if invested_capital != 0:
                    roic = (nopat / invested_capital) * 100
                    roic_list.append(round(roic, 2))

        # P/E Ratios
        for income in income_reports[:5]:
            if income.reported_eps:
                # assuming stock price $100 for now
                pe = 100 / float(income.reported_eps)
                pe_ratios.append(round(pe, 2))

    return render(request, 'financials.html', {
        'symbol': symbol,
        'income_reports': income_reports,
        'balance_reports': balance_reports,
        'cashflow_reports': cashflow_reports,
        'revenue_growth': revenue_growth,
        'earnings_growth': earnings_growth,
        'shares_change': shares_change,
        'free_cashflow_growth': free_cashflow_growth,
        'roic_list': roic_list,
        'pe_ratios': pe_ratios,
    })
