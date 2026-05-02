import pandas as pd
import yfinance as yf


def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    if getattr(df.columns, "nlevels", 1) > 1:
        df = df.copy()
        df.columns = [str(t[0]) for t in df.columns.to_list()]
    return df


def normalize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    df = _flatten_columns(df)

    required = ["Open", "High", "Low", "Close", "Volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing columns: {missing}. Available: {list(df.columns)}")

    out = df.loc[:, required].copy()
    out.index = pd.to_datetime(out.index)
    out = out.sort_index()
    return out


def download_ohlcv(symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False)
    if df is None or df.empty:
        raise ValueError(f"No data returned for symbol={symbol!r}, period={period!r}, interval={interval!r}")
    return normalize_ohlcv(df)
