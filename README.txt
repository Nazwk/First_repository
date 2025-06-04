# Portfolio Analysis Script

This repository contains a simple Python script (`portfolio_analysis.py`) that reads a CSV file of stock tickers and optional weights, fetches price data from Yahoo Finance using the `yfinance` library, and compares the cumulative return of the portfolio against the S&P 500 index.

## Requirements

- Python 3.11+
- `yfinance` and `pandas` (install with `pip install yfinance pandas`)

## CSV Format

```
ticker,weight
BHP,0.5
CBA,0.5
```

If no `weight` column is provided, the script assumes equal weights.

## Running the script

```bash
python3 portfolio_analysis.py portfolio.csv --start 2022-01-01 --end 2023-01-01
```

The script prints the cumulative returns of the portfolio and the S&P 500. If `matplotlib` is installed, it will also display a plot.

## Data Source

The script uses the free Yahoo Finance API via the `yfinance` package. ASX tickers are automatically suffixed with `.AX` when requesting data.
