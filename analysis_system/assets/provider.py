from dataclasses import dataclass
from abc import ABC, abstractmethod
import pandas as pd
import yfinance as yf




@dataclass
class Provider(ABC):

    @abstractmethod
    def get_prices(self, symbol: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def test_symbol(self, symbol: str) -> str:
        pass

@dataclass
class YahooProvider(Provider):

    period: str = "1d"
    interval: str = "1m"

    def get_prices(self, symbol: str) -> pd.DataFrame:
        data = yf.download(symbol, period=self.period, interval=self.interval)
        if data.empty:
            raise ValueError(f"Failed to fetch data for {symbol}")
        return data

    def test_symbol(self, symbol: str) -> str:
        try:
            data = self.get_prices(symbol)
            if data.empty:
                raise ValueError
            return symbol
        except Exception:
            raise ValueError(f"Symbol {symbol} not found")

@dataclass
class BinanceProvider(Provider):
    pass
