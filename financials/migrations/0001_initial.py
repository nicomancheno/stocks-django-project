# Generated by Django 4.2.7 on 2025-04-27 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiscal_date_ending', models.DateField()),
                ('total_revenue', models.FloatField(blank=True, null=True)),
                ('cost_of_revenue', models.FloatField(blank=True, null=True)),
                ('gross_profit', models.FloatField(blank=True, null=True)),
                ('net_income', models.FloatField(blank=True, null=True)),
                ('basic_average_shares', models.FloatField(blank=True, null=True)),
                ('basic_eps', models.FloatField(blank=True, null=True)),
                ('operating_expense', models.FloatField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.company')),
            ],
        ),
        migrations.CreateModel(
            name='CashFlowStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiscal_date_ending', models.DateField()),
                ('operating_cashflow', models.FloatField(blank=True, null=True)),
                ('free_cashflow', models.FloatField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.company')),
            ],
        ),
        migrations.CreateModel(
            name='BalanceSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiscal_date_ending', models.DateField()),
                ('total_assets', models.FloatField()),
                ('total_liabilities_net_minority_interest', models.FloatField()),
                ('total_equity_gross_minority_interest', models.FloatField()),
                ('net_tangible_assets', models.FloatField()),
                ('common_stock_equity', models.FloatField()),
                ('long_term_debt', models.FloatField()),
                ('working_capital', models.FloatField()),
                ('total_capitalization', models.FloatField()),
                ('cash_and_cash_equivalents', models.FloatField()),
                ('retained_earnings', models.FloatField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.company')),
            ],
        ),
    ]
