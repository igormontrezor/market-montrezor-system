import argparse





def main() -> None:

    parser = argparse.ArgumentParser(prog="market-analyze")

    parser.add_argument("--symbol", default="BTC-USD")

    parser.add_argument("--period", default="1y")

    parser.add_argument("--interval", default="1d")

    args = parser.parse_args()



    from market_analyze.data.yfinance_adapter import download_ohlcv



    df = download_ohlcv(args.symbol, period=args.period, interval=args.interval)

    print(df.tail())
