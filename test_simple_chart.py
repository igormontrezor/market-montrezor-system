import sys

from market_analyze.indicators import BollingerBands
sys.path.append('./src')

from market_analyze.assets import MarketAsset, YahooProvider
from market_analyze.indicators import BollingerBands, Rsi
from market_analyze.signals import BollingerBandsSignal, RsiSignal
from market_analyze.plotting import ChartPlotter
import pandas as pd

# Teste simples do gráfico
print("=== TESTE SIMPLES DO GRÁFICO ===")

# Criar asset
provider = YahooProvider(period="6y", interval="1wk")
btc = MarketAsset("BTC-USD", provider=provider)

# Obter dados
df = btc.get_prices()
print(f"Shape do DataFrame: {df.shape}")
print(f"Colunas: {df.columns.tolist()}")

# Calcular RSI simples
bb = BollingerBands()
bb_values = bb.calculate(btc)

print(f"BB shape: {bb_values.shape}")
print(f"BB últimos valores: {bb_values.tail()}")

# Criar sinais RSI simples
bb_signal = BollingerBandsSignal(bb=bb)
bb_signals = bb_signal.generate_signals(btc)

print(f"Sinais shape: {bb_signals.shape}")
print(f"Sinais únicos: {bb_signals.unique()}")
print(f"Sinais de compra: {(bb_signals == -1).sum()}")
print(f"Sinais de venda: {(bb_signals == 1).sum()}")

# Criar sinais booleanos
buy_signals = bb_signals == -1
sell_signals = bb_signals == 1

print(f"Buy signals bool: {buy_signals.sum()}")
print(f"Sell signals bool: {sell_signals.sum()}")

# Mostrar datas dos sinais
if buy_signals.sum() > 0:
    buy_dates = buy_signals[buy_signals].index
    print(f"Buy dates: {buy_dates}")

if sell_signals.sum() > 0:
    sell_dates = sell_signals[sell_signals].index
    print(f"Sell dates: {sell_dates}")

# Plotar gráfico simples sem sinais primeiro
print("\n=== PLOTANDO GRÁFICO SEM SINAIS ===")
try:
    ChartPlotter.plot_candlestick_with_signals(
        df=df,
        title="BTC-USD - Teste Simples",
        show_volume=True
    )
    print("Gráfico sem sinais plotado com sucesso!")
except Exception as e:
    print(f"Erro ao plotar gráfico sem sinais: {e}")
    import traceback
    traceback.print_exc()

# Plotar gráfico com sinais
if buy_signals.sum() > 0 or sell_signals.sum() > 0:
    print("\n=== PLOTANDO GRÁFICO COM SINAIS ===")
    try:
        ChartPlotter.plot_candlestick_with_signals(
            df=df,
            title="BTC-USD - Com Sinais",
            buy_signals=buy_signals,
            sell_signals=sell_signals,
            show_volume=True
        )
        print("Gráfico com sinais plotado com sucesso!")
    except Exception as e:
        print(f"Erro ao plotar gráfico com sinais: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\nNão há sinais para plotar")
