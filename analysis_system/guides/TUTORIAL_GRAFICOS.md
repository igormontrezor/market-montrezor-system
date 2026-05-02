# TUTORIAL COMPLETO - COMO USAR A PARTE GRÁFICA

## 1. INTRODUÇÃO

O sistema tem uma classe `ChartPlotter` em `src/market_analyze/plotting/charts.py` com métodos estáticos para criar gráficos.

## 2. MÉTODOS DISPONÍVEIS

### 2.1 `plot_candlestick_with_signals()`
**Ideal para:** Gráficos de candlestick com sinais de compra/venda

**Parâmetros:**
```python
ChartPlotter.plot_candlestick_with_signals(
    df: pd.DataFrame,              # DataFrame com dados OHLCV
    title: str,                   # Título do gráfico
    buy_signals: pd.Series = None,   # Sinais de compra (opcional)
    sell_signals: pd.Series = None,  # Sinais de venda (opcional)
    show_volume: bool = False        # Mostrar volume (opcional)
)
```

### 2.2 `plot_indicator_with_signals()`
**Ideal para:** Gráfico de preço + indicador + sinais

**Parâmetros:**
```python
ChartPlotter.plot_indicator_with_signals(
    df: pd.DataFrame,              # DataFrame com dados OHLCV
    indicator: pd.Series,           # Série do indicador
    title: str,                   # Título do gráfico
    buy_signals: pd.Series = None,   # Sinais de compra (opcional)
    sell_signals: pd.Series = None,  # Sinais de venda (opcional)
    indicator_name: str = "Indicator" # Nome do indicador
)
```

### 2.3 `plot_multiple_indicators()`
**Ideal para:** Múltiplos indicadores em subplots

**Parâmetros:**
```python
ChartPlotter.plot_multiple_indicators(
    data: Dict[str, pd.Series],    # Dicionário com indicadores
    title: str,                   # Título do gráfico
    subplot_titles: List[str] = None # Títulos dos subplots (opcional)
)
```

## 3. EXEMPLOS PRÁTICOS

### 3.1 EXEMPLO 1: Gráfico de Candlestick com Sinais RSI

```python
from market_analyze.plotting import ChartPlotter
from market_analyze.assets import MarketAsset
from market_analyze.assets.provider import YahooProvider
from market_analyze.strategies import BtcStrategy

# Criar dados
btc_strategy = BtcStrategy()
btc_provider = YahooProvider(period="6mo", interval="1d")
btc = MarketAsset("BTC-USD", provider=btc_provider)

# Obter dados e sinais
df = btc.get_prices()
rsi_values = btc_strategy.get_indicator_default('daily', 'rsi').calculate(btc)
rsi_signals = btc_strategy.get_signal('daily', 'rsi').generate_signals(btc)

# Criar sinais booleanos
buy_signals = rsi_signals == -1  # Sinais de compra
sell_signals = rsi_signals == 1   # Sinais de venda

# Plotar gráfico
ChartPlotter.plot_candlestick_with_signals(
    df=df,
    title="BTC-USD com Sinais RSI",
    buy_signals=buy_signals,
    sell_signals=sell_signals,
    show_volume=True
)
```

### 3.2 EXEMPLO 2: Gráfico de Preço com RSI

```python
# Usando os mesmos dados do exemplo anterior...

# Plotar preço com RSI
ChartPlotter.plot_indicator_with_signals(
    df=df,
    indicator=rsi_values,
    title="BTC-USD - Preço com RSI",
    buy_signals=buy_signals,
    sell_signals=sell_signals,
    indicator_name="RSI(14)"
)
```

### 3.3 EXEMPLO 3: Múltiplos Indicadores

```python
from market_analyze.indicators import SimpleMovingAverage, ExponentialMovingAverage

# Calcular múltiplos indicadores
sma_20 = SimpleMovingAverage(period=20).calculate(btc)
ema_20 = ExponentialMovingAverage(period=20).calculate(btc)
bb_values = BollingerBands(window=20, std_dev=2).calculate(btc)

# Criar dicionário com indicadores
indicators_data = {
    'SMA(20)': sma_20,
    'EMA(20)': ema_20,
    'BB%': bb_values
}

# Plotar múltiplos indicadores
ChartPlotter.plot_multiple_indicators(
    data=indicators_data,
    title="BTC-USD - Múltiplos Indicadores",
    subplot_titles=['SMA(20)', 'EMA(20)', 'Bollinger Bands %']
)
```

### 3.4 EXEMPLO 4: Bollinger Bands com Sinais

```python
from market_analyze.indicators import BollingerBands
from market_analyze.signals import BollingerBandsSignal

# Calcular Bollinger Bands
bb = BollingerBands(window=20, std_dev=2)
bb_values = bb.calculate(btc)

# Gerar sinais
bb_signal = BollingerBandsSignal(bb=bb)
bb_signals = bb_signal.generate_signals(btc)

# Sinais booleanos
bb_buy = bb_signals == -1
bb_sell = bb_signals == 1

# Plotar
ChartPlotter.plot_candlestick_with_signals(
    df=df,
    title="BTC-USD com Sinais Bollinger Bands",
    buy_signals=bb_buy,
    sell_signals=bb_sell,
    show_volume=True
)
```

### 3.5 EXEMPLO 5: MACD com Histograma

```python
from market_analyze.indicators import Macd
from market_analyze.signals import MacdSignal

# Calcular MACD
macd = Macd()
macd_values = macd.calculate(btc)

# Gerar sinais
macd_signal = MacdSignal(macd)
macd_signals = macd_signal.generate_signals(btc)

# Preparar dados para plotagem
macd_data = {
    'MACD Line': macd_values['macd'],
    'Signal Line': macd_values['signal'],
    'Histogram': macd_values['histogram']
}

# Plotar múltiplos componentes do MACD
ChartPlotter.plot_multiple_indicators(
    data=macd_data,
    title="BTC-USD - MACD",
    subplot_titles=['MACD Line', 'Signal Line', 'Histogram']
)
```

## 4. ESTRUTURA DE DADOS NECESSÁRIA

### 4.1 DataFrame para Candlestick
```python
# Precisa ter colunas: Open, High, Low, Close (Volume opcional)
df = btc.get_prices()
print(df.columns)
# Saída: Index(['Open', 'High', 'Low', 'Close', 'Volume'], dtype='object')
```

### 4.2 Series para Indicadores
```python
# Indicadores devem ser pandas.Series
rsi_values = btc_strategy.get_indicator_default('daily', 'rsi').calculate(btc)
print(type(rsi_values))  # <class 'pandas.core.series.Series'>
print(rsi_values.name)  # 'RSI_14'
```

### 4.3 Series para Sinais
```python
# Sinais devem ser pandas.Series com valores: -1 (compra), 0 (neutro), 1 (venda)
rsi_signals = btc_strategy.get_signal('daily', 'rsi').generate_signals(btc)
print(rsi_signals.unique())  # [-1, 0, 1]
```

## 5. DICAS AVANÇADAS

### 5.1 Personalizar Cores
```python
# Os gráficos usam cores padrão, mas você pode modificar no código charts.py
# Cores atuais (em charts.py):
# buy_signals: cor verde
# sell_signals: cor vermelha
```

### 5.2 Múltiplos Timeframes
```python
# Para diferentes timeframes, use providers diferentes:
btc_daily = MarketAsset("BTC-USD", provider=YahooProvider(period="6mo", interval="1d"))
btc_weekly = MarketAsset("BTC-USD", provider=YahooProvider(period="2y", interval="1wk"))
btc_monthly = MarketAsset("BTC-USD", provider=YahooProvider(period="5y", interval="1mo"))
```

### 5.3 Combinar Indicadores
```python
# Plotar indicador com sinais de outro indicador
rsi_values = btc_strategy.get_indicator_default('daily', 'rsi').calculate(btc)
macd_signals = btc_strategy.get_signal('daily', 'macd').generate_signals(btc)

ChartPlotter.plot_indicator_with_signals(
    df=df,
    indicator=rsi_values,
    title="RSI com Sinais MACD",
    buy_signals=macd_signals == -1,
    sell_signals=macd_signals == 1,
    indicator_name="RSI(14)"
)
```

## 6. RESUMO DOS PARÂMETROS

| Método | df | indicator | title | buy_signals | sell_signals | show_volume | data |
|--------|-----|-----------|--------|-------------|---------------|--------------|-------|
| `plot_candlestick_with_signals` | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| `plot_indicator_with_signals` | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| `plot_multiple_indicators` | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ |

## 7. EXEMPLO COMPLETO FINAL

```python
from market_analyze.plotting import ChartPlotter
from market_analyze.assets import MarketAsset
from market_analyze.assets.provider import YahooProvider
from market_analyze.strategies import BtcStrategy

# 1. Configurar asset
btc = MarketAsset("BTC-USD", provider=YahooProvider(period="6mo", interval="1d"))
df = btc.get_prices()

# 2. Configurar estratégia
strategy = BtcStrategy()

# 3. Calcular indicadores e sinais
rsi = strategy.get_indicator_default('daily', 'rsi').calculate(btc)
rsi_buy = strategy.get_signal('daily', 'rsi').generate_signals(btc) == -1
rsi_sell = strategy.get_signal('daily', 'rsi').generate_signals(btc) == 1

bb = strategy.get_indicator_default('daily', 'bb').calculate(btc)
bb_buy = strategy.get_signal('daily', 'bb').generate_signals(btc) == -1
bb_sell = strategy.get_signal('daily', 'bb').generate_signals(btc) == 1

# 4. Plotar gráficos
print("=== GRÁFICO 1: Candlestick com Sinais RSI ===")
ChartPlotter.plot_candlestick_with_signals(
    df=df,
    title="BTC-USD com Sinais RSI",
    buy_signals=rsi_buy,
    sell_signals=rsi_sell,
    show_volume=True
)

print("=== GRÁFICO 2: RSI com Sinais ===")
ChartPlotter.plot_indicator_with_signals(
    df=df,
    indicator=rsi,
    title="BTC-USD - RSI",
    buy_signals=rsi_buy,
    sell_signals=rsi_sell,
    indicator_name="RSI(14)"
)

print("=== GRÁFICO 3: Múltiplos Indicadores ===")
indicators_data = {
    'RSI': rsi,
    'BB%': bb
}
ChartPlotter.plot_multiple_indicators(
    data=indicators_data,
    title="BTC-USD - Indicadores"
)
```

**Com este tutorial você consegue usar 100% da parte gráfica do sistema!**
