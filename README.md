# Personal Finance & Investment System

A menu-driven Python console application for exploring stock information, tracking a sample portfolio, and managing day-to-day expenses.

## Features

- **Stock analysis:** company overview, recent price history and charts, financial statements, analyst recommendations, valuation and profitability metrics, moving averages, and historical risk and return analysis.
- **Portfolio and trade tracking:** record stock holdings and trades, view current portfolio valuation, review realized and unrealized profit or loss, and see transaction history and sector allocation.
- **Expense management:** add, view, search, edit, or delete expenses; review daily and monthly reports; analyze spending by category; set monthly spending limits; calculate a monthly savings rate; and manage recurring expenses.

## Requirements

- Python 3
- The packages listed in **requirements.txt**
- An internet connection for current and historical stock data from Yahoo Finance

## Run the application

From the project folder, install the dependencies and start the main program:

~~~bash
python -m pip install -r requirements.txt
python finance.py
~~~

You can optionally create and activate a virtual environment first:

~~~bash
python -m venv .venv
~~~

On Windows PowerShell, activate it with .venv/Scripts/Activate.ps1. On macOS or Linux, use source .venv/bin/activate.

## Main menu

When the program starts, choose one of the three areas:

1. Share price and fundamental analysis
2. Stock portfolio and trading tracker
3. Daily expense and threshold tracker

The expense features are implemented in **expense.py** and are connected to the main application in **finance.py**.

## Data and usage notes

- Portfolio, trade, expense, threshold, and recurring-expense records are kept in memory while the program is running. They are not saved between runs.
- Stock information is retrieved online, so availability depends on the data source and network connection.
- Risk and return figures describe historical data and are not predictions or investment advice.
