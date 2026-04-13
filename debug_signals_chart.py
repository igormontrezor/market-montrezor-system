import sys
sys.path.append('./src')

from market_analyze.assets import Crypto, YahooProvider
from market_analyze.indicators import Rsi, Macd
from market_analyze.signals import RsiSignal, MacdSignal, CombinedSignal
from market_analyze.plotting import ChartPlotter
import pandas as pd

# Debug específico para sinais no gráfico
print("=== DEBUG DE SINAIS NO GRÁFICO ===")

# Criar asset
provider = YahooProvider(period="6mo", interval="1wk")
btc = Crypto("BTC-USD", provider=provider)

# Obter dados
df = btc.get_prices()
print(f"Shape do DataFrame: {df.shape}")
print(f"Colunas: {df.columns.tolist()}")

# Calcular indicadores
rsi = Rsi(period=14)
macd = Macd()

# Criar sinais com thresholds mais permissivos
rsi_signal = RsiSignal(rsi=rsi, buy_threshold=35, sell_threshold=65)
macd_signal = MacdSignal(macd=macd)

rsi_signals = rsi_signal.generate_signals(btc)
macd_signals = macd_signal.generate_signals(btc)

print(f"\nRSI Signals - Shape: {rsi_signals.shape}")
print(f"RSI Signals - Únicos: {rsi_signals.unique()}")
print(f"RSI Signals - Compras: {(rsi_signals == -1).sum()}")
print(f"RSI Signals - Vendas: {(rsi_signals == 1).sum()}")

print(f"\nMACD Signals - Shape: {macd_signals.shape}")
print(f"MACD Signals - Únicos: {macd_signals.unique()}")
print(f"MACD Signals - Compras: {(macd_signals == 1).sum()}")
print(f"MACD Signals - Vendas: {(macd_signals == -1).sum()}")

# Sinal combinado
combined = CombinedSignal(
    signals=[rsi_signal, macd_signal],
    weights=[1.0, 1.0],
    quantity_threshold=1.5
)
combined_signals = combined.generate_signals(btc)

print(f"\nCombined Signals - Shape: {combined_signals.shape}")
print(f"Combined Signals - Únicos: {combined_signals.unique()}")
print(f"Combined Signals - Compras: {(combined_signals == -1).sum()}")
print(f"Combined Signals - Vendas: {(combined_signals == 1).sum()}")

# Debug dos sinais booleanos
buy_signals_bool = combined_signals == -1
sell_signals_bool = combined_signals == 1

print(f"\nBuy Signals Boolean - Shape: {buy_signals_bool.shape}")
print(f"Buy Signals Boolean - True count: {buy_signals_bool.sum()}")
print(f"Buy Signals Boolean - Index where True: {buy_signals_bool[buy_signals_bool].index.tolist()}")

print(f"\nSell Signals Boolean - Shape: {sell_signals_bool.shape}")
print(f"Sell Signals Boolean - True count: {sell_signals_bool.sum()}")
print(f"Sell Signals Boolean - Index where True: {sell_signals_bool[sell_signals_bool].index.tolist()}")

# Testar acesso aos dados do DataFrame
print(f"\n=== TESTE DE ACESSO AOS DADOS ===")

# Verificar se o DataFrame tem MultiIndex
if isinstance(df.columns, pd.MultiIndex):
    print("DataFrame tem MultiIndex columns")
    symbol = df.columns.get_level_values(1)[0]
    close_col = ('Close', symbol)
    print(f"Símbolo: {symbol}")
    print(f"Coluna Close: {close_col}")
else:
    print("DataFrame tem colunas normais")
    close_col = 'Close'
    print(f"Coluna Close: {close_col}")

# Testar acesso aos dados com sinais
if buy_signals_bool.sum() > 0:
    buy_dates = buy_signals_bool[buy_signals_bool].index
    print(f"\nBuy dates: {buy_dates}")
    
    # Tentar acessar preços
    try:
        if isinstance(df.columns, pd.MultiIndex):
            buy_prices = df.loc[buy_dates, close_col]
        else:
            buy_prices = df.loc[buy_dates, 'Close']
        print(f"Buy prices: {buy_prices.values}")
        print(f"Buy prices type: {type(buy_prices)}")
    except Exception as e:
        print(f"Erro ao acessar buy prices: {e}")

if sell_signals_bool.sum() > 0:
    sell_dates = sell_signals_bool[sell_signals_bool].index
    print(f"\nSell dates: {sell_dates}")
    
    # Tentar acessar preços
    try:
        if isinstance(df.columns, pd.MultiIndex):
            sell_prices = df.loc[sell_dates, close_col]
        else:
            sell_prices = df.loc[sell_dates, 'Close']
        print(f"Sell prices: {sell_prices.values}")
        print(f"Sell prices type: {type(sell_prices)}")
    except Exception as e:
        print(f"Erro ao acessar sell prices: {e}")

# Plotar gráfico
print(f"\n=== PLOTANDO GRÁFICO ===")
try:
    ChartPlotter.plot_candlestick_with_signals(
        df=df,
        title="BTC-USD - Debug de Sinais",
        buy_signals=buy_signals_bool,
        sell_signals=sell_signals_bool,
        show_volume=True
    )
    print("Gráfico plotado com sucesso!")
except Exception as e:
    print(f"Erro ao plotar gráfico: {e}")
    import traceback
    traceback.print_exc()
