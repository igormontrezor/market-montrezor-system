import sys
sys.path.append('./src')

from market_analyze.assets import Crypto, YahooProvider
from market_analyze.indicators import Rsi
from market_analyze.signals import RsiSignal
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Debug detalhado do gráfico
print("=== DEBUG DETALHADO DO GRÁFICO ===")

# Criar asset
provider = YahooProvider(period="6mo", interval="1wk")
btc = Crypto("BTC-USD", provider=provider)

# Obter dados
df = btc.get_prices()
print(f"Shape do DataFrame: {df.shape}")
print(f"Colunas: {df.columns.tolist()}")

# Calcular RSI
rsi = Rsi(period=14)
rsi_values = rsi.calculate(btc)

# Criar sinais
rsi_signal = RsiSignal(rsi=rsi, buy_threshold=30, sell_threshold=70)
rsi_signals = rsi_signal.generate_signals(btc)

# Sinais booleanos
buy_signals = rsi_signals == -1
sell_signals = rsi_signals == 1

print(f"Buy signals: {buy_signals.sum()}")
print(f"Sell signals: {sell_signals.sum()}")

# Configurar colunas para MultiIndex
if isinstance(df.columns, pd.MultiIndex):
    symbol = df.columns.get_level_values(1)[0]
    open_col = ('Open', symbol)
    high_col = ('High', symbol)
    low_col = ('Low', symbol)
    close_col = ('Close', symbol)
    volume_col = ('Volume', symbol)
    print(f"Usando MultiIndex - símbolo: {symbol}")
else:
    open_col = 'Open'
    high_col = 'High'
    low_col = 'Low'
    close_col = 'Close'
    volume_col = 'Volume'
    print("Usando colunas normais")

# Criar figura manualmente
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    subplot_titles=('BTC-USD - Manual', 'Volume'),
    row_width=[0.2, 0.7]
)

# Adicionar candlestick
print("Adicionando candlestick...")
fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df[open_col],
        high=df[high_col],
        low=df[low_col],
        close=df[close_col],
        name='Price'
    ),
    row=1, col=1
)

# Adicionar sinais de compra manualmente
if buy_signals.sum() > 0:
    buy_dates = buy_signals[buy_signals].index
    print(f"Buy dates: {buy_dates}")
    
    # Tentar diferentes formas de acessar os preços
    try:
        buy_prices = df.loc[buy_dates, close_col]
        print(f"Buy prices type: {type(buy_prices)}")
        print(f"Buy prices: {buy_prices}")
        
        if isinstance(buy_prices, pd.Series):
            buy_prices = buy_prices.values
            print(f"Buy prices after .values: {buy_prices}")
        
        fig.add_trace(
            go.Scatter(
                x=buy_dates,
                y=buy_prices,
                mode='markers',
                marker=dict(symbol='triangle-up', size=15, color='green'),
                name='Buy Signal'
            ),
            row=1, col=1
        )
        print("Sinais de compra adicionados com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar sinais de compra: {e}")
        import traceback
        traceback.print_exc()

# Adicionar sinais de venda manualmente
if sell_signals.sum() > 0:
    sell_dates = sell_signals[sell_signals].index
    print(f"Sell dates: {sell_dates}")
    
    try:
        sell_prices = df.loc[sell_dates, close_col]
        print(f"Sell prices type: {type(sell_prices)}")
        print(f"Sell prices: {sell_prices}")
        
        if isinstance(sell_prices, pd.Series):
            sell_prices = sell_prices.values
            print(f"Sell prices after .values: {sell_prices}")
        
        fig.add_trace(
            go.Scatter(
                x=sell_dates,
                y=sell_prices,
                mode='markers',
                marker=dict(symbol='triangle-down', size=15, color='red'),
                name='Sell Signal'
            ),
            row=1, col=1
        )
        print("Sinais de venda adicionados com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar sinais de venda: {e}")
        import traceback
        traceback.print_exc()

# Adicionar volume
if volume_col in df.columns:
    print("Adicionando volume...")
    fig.add_trace(
        go.Bar(x=df.index, y=df[volume_col], name='Volume'),
        row=2, col=1
    )

# Atualizar layout e mostrar
fig.update_layout(
    title='BTC-USD - Debug Manual',
    yaxis_title='Price',
    xaxis_rangeslider_visible=False,
    height=600
)

print("Mostrando gráfico...")
fig.show()
print("Gráfico mostrado!")
