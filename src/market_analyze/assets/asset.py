from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, List
import pandas as pd
import logging


@dataclass
class Asset(ABC):
    symbol: str
    _prices: Optional[pd.DataFrame] = None

    @abstractmethod
    def get_prices(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def test_symbol(self) -> str:
        pass

    def get_close_series(self) -> pd.Series:
        prices = self.get_prices()
        close_col = ('Close', self.symbol) if ('Close', self.symbol) in prices.columns else 'Close'
        if close_col not in prices.columns:
            raise ValueError("Missing 'Close' column in price data")
        return prices[close_col]

    def get_current_price(self) -> float:
        prices = self.get_prices()
        close_col = ('Close', self.symbol) if ('Close', self.symbol) in prices.columns else 'Close'
        return float(prices[close_col].iloc[-1])


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
        import yfinance as yf
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
class Crypto(Asset):
    provider: Optional[Provider] = None

    def __post_init__(self):
        if self.provider is None:
            self.provider = YahooProvider()

    def get_prices(self) -> pd.DataFrame:
        if self._prices is None:
            logging.info(f"Fetching prices for {self.symbol}...")
            self._prices = self.provider.get_prices(self.symbol)
        return self._prices

    def test_symbol(self) -> str:
        return self.provider.test_symbol(self.symbol)


@dataclass
class Btc(Crypto):
    pass


@dataclass
class Portfolio:
    name: str
    positions: List['Position'] = field(default_factory=list)

    def add_position(self, position: 'Position'):
        if position.quantity <= 0:
            raise ValueError("quantity must be positive")
        self.positions.append(position)

    def del_position(self, position: 'Position'):
        if position not in self.positions:
            raise ValueError("Position not found")
        self.positions.remove(position)

    def total_value(self) -> float:
        return sum(position.total_value() for position in self.positions)

    def total_pnl(self) -> float:
        return sum(position.calculate_pnl() for position in self.positions)

    def __getitem__(self, index: int) -> 'Position':
        return self.positions[index]


@dataclass
class Position(ABC):
    asset: Asset
    quantity: float = 1

    @abstractmethod
    def calculate_pnl(self) -> float:
        pass

    def total_value(self) -> float:
        return self.asset.get_current_price() * self.quantity


@dataclass
class LongPosition(Position):
    entry_price: float = None

    def __post_init__(self):
        if self.entry_price is None:
            self.entry_price = self.asset.get_current_price()

    def calculate_pnl(self) -> float:
        return (self.asset.get_current_price() - self.entry_price) * self.quantity


@dataclass
class ShortPosition(Position):
    entry_price: float = None

    def __post_init__(self):
        if self.entry_price is None:
            self.entry_price = self.asset.get_current_price()

    def calculate_pnl(self) -> float:
        return (self.entry_price - self.asset.get_current_price()) * self.quantity
