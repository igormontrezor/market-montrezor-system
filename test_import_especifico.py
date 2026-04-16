# Teste com imports específicos para evitar o erro
from market_analyze.plotting import ChartPlotter
from market_analyze.strategies import BtcStrategy
from market_analyze.assets import MarketAsset
from market_analyze.assets.provider import YahooProvider

print("Imports funcionaram!")

# Testar:
btc_strategy = BtcStrategy()
btc_weekly_provider = YahooProvider(period="8y", interval="1wk")
btc_weekly = MarketAsset("BTC-USD", provider=btc_weekly_provider)

btc_rsi_weekly_values = btc_strategy.get_indicator_default('weekly', 'sharpe').calculate(btc_weekly)
btc_rsi_weekly_signals = btc_strategy.get_signal('weekly', 'sharpe').generate_signals(btc_weekly)

print("RSI Values:")
print(btc_rsi_weekly_values.tail())
print("\nRSI Signals:")
print(btc_rsi_weekly_signals.tail())
