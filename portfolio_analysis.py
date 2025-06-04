import argparse
import pandas as pd
import yfinance as yf


def read_portfolio(csv_path):
    """Read a CSV with tickers and optional weight column."""
    df = pd.read_csv(csv_path)
    df.columns = [c.lower() for c in df.columns]
    if 'weight' not in df.columns:
        df['weight'] = 1.0 / len(df)
    else:
        # normalize weights to sum to 1
        df['weight'] = df['weight'] / df['weight'].sum()
    return df


def get_price_data(tickers, start, end):
    """Fetch adjusted close prices for a list of tickers."""
    data = yf.download(tickers, start=start, end=end, progress=False)['Adj Close']
    if isinstance(data, pd.Series):
        data = data.to_frame()
    return data


def compute_portfolio_returns(prices, weights):
    returns = prices.pct_change().dropna()
    weighted = returns.mul(weights, axis=1)
    port_returns = weighted.sum(axis=1)
    cumulative = (1 + port_returns).cumprod()
    return cumulative


def main(csv_path, start, end):
    portfolio = read_portfolio(csv_path)
    tickers = portfolio['ticker'].tolist()

    # Append .AX for ASX tickers if not provided
    adj_tickers = [t if '.' in t else f"{t}.AX" for t in tickers]

    prices = get_price_data(adj_tickers, start, end)
    prices.columns = tickers  # rename to original tickers
    portfolio_ret = compute_portfolio_returns(prices, portfolio['weight'])

    # Benchmark: S&P 500 (^GSPC)
    benchmark_prices = get_price_data('^GSPC', start, end)
    benchmark_ret = (1 + benchmark_prices.pct_change().dropna()).cumprod().squeeze()

    result = pd.DataFrame({'Portfolio': portfolio_ret, 'S&P 500': benchmark_ret})
    print(result.tail())

    # Optionally plot results if matplotlib is available
    try:
        import matplotlib.pyplot as plt
        result.plot(title='Portfolio vs S&P 500')
        plt.ylabel('Cumulative Return')
        plt.show()
    except Exception as e:
        print("Could not generate plot:", e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Portfolio analysis vs S&P 500')
    parser.add_argument('csv', help='CSV file with columns: ticker[, weight]')
    parser.add_argument('--start', default='2022-01-01', help='Start date YYYY-MM-DD')
    parser.add_argument('--end', default=None, help='End date YYYY-MM-DD')
    args = parser.parse_args()
    main(args.csv, args.start, args.end)
