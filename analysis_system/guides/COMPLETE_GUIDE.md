# Guia Completo de Uso - Complete Usage Guide

## Sumário / Table of Contents
1. [Configuração Inicial / Initial Setup](#configuração-inicial--initial-setup)
2. [Uso via Linha de Comando / Command Line Usage](#uso-via-linha-de-comando--command-line-usage)
3. [Uso Programático / Programmatic Usage](#uso-programático--programmatic-usage)
4. [Indicadores Técnicos / Technical Indicators](#indicadores-técnicos--technical-indicators)
5. [Sinais de Trading / Trading Signals](#sinais-de-trading--trading-signals)
6. [Visualizações / Visualizations](#visualizações--visualizations)
7. [Portfólio e Posições / Portfolio and Positions](#portfólio-e-posições--portfolio-and-positions)
8. [Exemplos Avançados / Advanced Examples](#exemplos-avançados--advanced-examples)

---

## Configuração Inicial / Initial Setup

### Português:
1. **Ativar Ambiente Virtual:**
   ```bash
   # Windows
   .venv\Scripts\activate.bat

   # Linux/Mac
   source .venv/bin/activate
   ```

2. **Verificar Instalação:**
   ```bash
   cd src/market_analyze
   python -c "from market_analyze import Crypto, YahooProvider, Rsi; print('Sistema pronto!')"
   ```

### English:
1. **Activate Virtual Environment:**
   ```bash
   # Windows
   .venv\Scripts\activate.bat

   # Linux/Mac
   source .venv/bin/activate
   ```

2. **Verify Installation:**
   ```bash
   cd src/market_analyze
   python -c "from market_analyze import Crypto, YahooProvider, Rsi; print('System ready!')"
   ```

---

## Uso via Linha de Comando / Command Line Usage

### Português:

#### 1. Análise Simples:
```bash
# Análise básica de BTC
python main.py --symbol BTC-USD --period 1mo --interval 1d

# Análise com gráficos
python main.py --symbol SPY --period 6mo --interval 1wk --plot

# Análise de múltiplos ativos
python main.py --symbol AAPL --period 1y --interval 1d
```

#### 2. Executar Exemplos:
```bash
# Exemplo básico completo
python main.py --example basic

# Exemplo de estratégia avançada
python main.py --example strategy
```

#### 3. Opções Disponíveis:
- `--symbol`: Símbolo do ativo (ex: BTC-USD, SPY, AAPL)
- `--period`: Período de dados (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
- `--interval`: Intervalo dos dados (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
- `--plot`: Mostrar gráficos interativos
- `--example`: Executar exemplo pré-definido (basic, strategy)

### English:

#### 1. Simple Analysis:
```bash
# Basic BTC analysis
python main.py --symbol BTC-USD --period 1mo --interval 1d

# Analysis with charts
python main.py --symbol SPY --period 6mo --interval 1wk --plot

# Multiple assets analysis
python main.py --symbol AAPL --period 1y --interval 1d
```

#### 2. Run Examples:
```bash
# Complete basic example
python main.py --example basic

# Advanced strategy example
python main.py --example strategy
```

#### 3. Available Options:
- `--symbol`: Asset symbol (e.g., BTC-USD, SPY, AAPL)
- `--period`: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
- `--interval`: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
- `--plot`: Show interactive charts
- `--example`: Run predefined example (basic, strategy)

---

## Uso Programático / Programmatic Usage

### Português:

#### 1. Importação Básica:
```python
from market_analyze import (
    Crypto, YahooProvider, Portfolio, LongPosition, ShortPosition,
    SimpleMovingAverage, Rsi, Macd, BollingerBands, SharpeRatio, SortinoRatio,
    RsiSignal, MacdSignal, CombinedSignal, ChartPlotter
)
```

#### 2. Criar e Analisar um Ativo:
```python
# Criar provider e asset
provider = YahooProvider(period="1y", interval="1wk")
btc = Crypto("BTC-USD", provider=provider)

# Obter dados
current_price = btc.get_current_price()
price_data = btc.get_prices()
close_series = btc.get_close_series()

print(f"Preço Atual: ${current_price:.2f}")
print(f"Dados Shape: {price_data.shape}")
```

### English:

#### 1. Basic Import:
```python
from market_analyze import (
    Crypto, YahooProvider, Portfolio, LongPosition, ShortPosition,
    SimpleMovingAverage, Rsi, Macd, BollingerBands, SharpeRatio, SortinoRatio,
    RsiSignal, MacdSignal, CombinedSignal, ChartPlotter
)
```

#### 2. Create and Analyze an Asset:
```python
# Create provider and asset
provider = YahooProvider(period="1y", interval="1wk")
btc = Crypto("BTC-USD", provider=provider)

# Get data
current_price = btc.get_current_price()
price_data = btc.get_prices()
close_series = btc.get_close_series()

print(f"Current Price: ${current_price:.2f}")
print(f"Data Shape: {price_data.shape}")
```

---

## Indicadores Técnicos / Technical Indicators

### Português:

#### 1. Médias Móveis:
```python
# Simple Moving Average
sma_20 = SimpleMovingAverage(period=20)
sma_50 = SimpleMovingAverage(period=50)
sma_200 = SimpleMovingAverage(period=200)

btc_sma_20 = sma_20.calculate(btc)
btc_sma_50 = sma_50.calculate(btc)
btc_sma_200 = sma_200.calculate(btc)

# Exponential Moving Average
ema_12 = ExponentialMovingAverage(period=12)
ema_26 = ExponentialMovingAverage(period=26)

btc_ema_12 = ema_12.calculate(btc)
btc_ema_26 = ema_26.calculate(btc)
```

#### 2. RSI (Relative Strength Index):
```python
# RSI com diferentes períodos
rsi_14 = Rsi(period=14)
rsi_21 = Rsi(period=21)

btc_rsi_14 = rsi_14.calculate(btc)
btc_rsi_21 = rsi_21.calculate(btc)

print(f"RSI 14: {btc_rsi_14.iloc[-1]:.2f}")
print(f"RSI 21: {btc_rsi_21.iloc[-1]:.2f}")
```

#### 3. Bandas de Bollinger:
```python
# Bollinger Bands
bb = BollingerBands(window=20, std_dev=2)
btc_bb = bb.calculate(btc)

print(f"BB %B: {btc_bb.iloc[-1]:.4f}")
```

#### 4. MACD:
```python
# MACD
macd = Macd(fast=12, slow=26, signal=9)
btc_macd = macd.calculate(btc)

macd_line = btc_macd['macd']
signal_line = btc_macd['signal']
histogram = btc_macd['histogram']

print(f"MACD: {macd_line.iloc[-1]:.4f}")
print(f"Signal: {signal_line.iloc[-1]:.4f}")
print(f"Histogram: {histogram.iloc[-1]:.4f}")
```

#### 5. Stochastic RSI:
```python
# Stochastic RSI
stoch_rsi = StochRsi(period=14, smooth=3)
btc_stoch = stoch_rsi.calculate(btc)

k_line = btc_stoch['k']
d_line = btc_stoch['d']

print(f"Stoch RSI K: {k_line.iloc[-1]:.2f}")
print(f"Stoch RSI D: {d_line.iloc[-1]:.2f}")
```

#### 6. Índices de Risco:
```python
# Sharpe Ratio
sharpe = SharpeRatio(period=52, window=60, rf=0.01)
btc_sharpe = sharpe.calculate(btc)

# Sortino Ratio
sortino = SortinoRatio(period=52, window=60, rf=0.01)
btc_sortino = sortino.calculate(btc)

print(f"Sharpe: {btc_sharpe.iloc[-1]:.4f}")
print(f"Sortino: {btc_sortino.iloc[-1]:.4f}")
```

### English:

#### 1. Moving Averages:
```python
# Simple Moving Average
sma_20 = SimpleMovingAverage(period=20)
sma_50 = SimpleMovingAverage(period=50)
sma_200 = SimpleMovingAverage(period=200)

btc_sma_20 = sma_20.calculate(btc)
btc_sma_50 = sma_50.calculate(btc)
btc_sma_200 = sma_200.calculate(btc)

# Exponential Moving Average
ema_12 = ExponentialMovingAverage(period=12)
ema_26 = ExponentialMovingAverage(period=26)

btc_ema_12 = ema_12.calculate(btc)
btc_ema_26 = ema_26.calculate(btc)
```

#### 2. RSI (Relative Strength Index):
```python
# RSI with different periods
rsi_14 = Rsi(period=14)
rsi_21 = Rsi(period=21)

btc_rsi_14 = rsi_14.calculate(btc)
btc_rsi_21 = rsi_21.calculate(btc)

print(f"RSI 14: {btc_rsi_14.iloc[-1]:.2f}")
print(f"RSI 21: {btc_rsi_21.iloc[-1]:.2f}")
```

#### 3. Bollinger Bands:
```python
# Bollinger Bands
bb = BollingerBands(window=20, std_dev=2)
btc_bb = bb.calculate(btc)

print(f"BB %B: {btc_bb.iloc[-1]:.4f}")
```

#### 4. MACD:
```python
# MACD
macd = Macd(fast=12, slow=26, signal=9)
btc_macd = macd.calculate(btc)

macd_line = btc_macd['macd']
signal_line = btc_macd['signal']
histogram = btc_macd['histogram']

print(f"MACD: {macd_line.iloc[-1]:.4f}")
print(f"Signal: {signal_line.iloc[-1]:.4f}")
print(f"Histogram: {histogram.iloc[-1]:.4f}")
```

#### 5. Stochastic RSI:
```python
# Stochastic RSI
stoch_rsi = StochRsi(period=14, smooth=3)
btc_stoch = stoch_rsi.calculate(btc)

k_line = btc_stoch['k']
d_line = btc_stoch['d']

print(f"Stoch RSI K: {k_line.iloc[-1]:.2f}")
print(f"Stoch RSI D: {d_line.iloc[-1]:.2f}")
```

#### 6. Risk Ratios:
```python
# Sharpe Ratio
sharpe = SharpeRatio(period=52, window=60, rf=0.01)
btc_sharpe = sharpe.calculate(btc)

# Sortino Ratio
sortino = SortinoRatio(period=52, window=60, rf=0.01)
btc_sortino = sortino.calculate(btc)

print(f"Sharpe: {btc_sharpe.iloc[-1]:.4f}")
print(f"Sortino: {btc_sortino.iloc[-1]:.4f}")
```

---

## Sinais de Trading / Trading Signals

### Português:

#### 1. Sinais Individuais:
```python
# Sinal RSI
rsi = Rsi(period=14)
rsi_signal = RsiSignal(rsi=rsi, buy_threshold=30, sell_threshold=70)
rsi_signals = rsi_signal.generate_signals(btc)

# Sinal MACD
macd = Macd()
macd_signal = MacdSignal(macd=macd)
macd_signals = macd_signal.generate_signals(btc)

# Sinal Bollinger Bands
bb = BollingerBands(window=20, std_dev=2)
bb_signal = BollingerBandsSignal(bb=bb, buy_threshold=0.1, sell_threshold=0.9)
bb_signals = bb_signal.generate_signals(btc)

# Sinal Stochastic RSI
stoch = StochRsi(period=14, smooth=3)
stoch_signal = StochRsiSignal(stoch=stoch, buy_threshold=20, sell_threshold=80)
stoch_signals = stoch_signal.generate_signals(btc)
```

#### 2. Sinais Combinados:
```python
# Estratégia simples (RSI + MACD)
simple_combined = CombinedSignal(
    signals=[rsi_signal, macd_signal],
    weights=[1.0, 1.0],
    quantity_threshold=2.0
)

# Estratégia completa (múltiplos sinais)
full_strategy = CombinedSignal(
    signals=[rsi_signal, macd_signal, bb_signal, stoch_signal],
    weights=[1.0, 1.0, 0.8, 0.8],
    quantity_threshold=3.0,
    window=2
)

# Gerar sinais
simple_signals = simple_combined.generate_signals(btc)
full_signals = full_strategy.confirm_signals(btc)  # Com confirmação
```

#### 3. Análise de Sinais:
```python
# Contar sinais
buy_signals = (signals == -1).sum()
sell_signals = (signals == 1).sum()
neutral_signals = (signals == 0).sum()

print(f"Sinais de Compra: {buy_signals}")
print(f"Sinais de Venda: {sell_signals}")
print(f"Sinais Neutros: {neutral_signals}")

# Último sinal
last_signal = signals.iloc[-1]
if last_signal == -1:
    print("Último sinal: COMPRA")
elif last_signal == 1:
    print("Último sinal: VENDA")
else:
    print("Último sinal: NEUTRO")

# Data do último sinal
last_signal_date = signals[signals != 0].index[-1] if len(signals[signals != 0]) > 0 else None
if last_signal_date:
    print(f"Data do último sinal: {last_signal_date}")
```

### English:

#### 1. Individual Signals:
```python
# RSI Signal
rsi = Rsi(period=14)
rsi_signal = RsiSignal(rsi=rsi, buy_threshold=30, sell_threshold=70)
rsi_signals = rsi_signal.generate_signals(btc)

# MACD Signal
macd = Macd()
macd_signal = MacdSignal(macd=macd)
macd_signals = macd_signal.generate_signals(btc)

# Bollinger Bands Signal
bb = BollingerBands(window=20, std_dev=2)
bb_signal = BollingerBandsSignal(bb=bb, buy_threshold=0.1, sell_threshold=0.9)
bb_signals = bb_signal.generate_signals(btc)

# Stochastic RSI Signal
stoch = StochRsi(period=14, smooth=3)
stoch_signal = StochRsiSignal(stoch=stoch, buy_threshold=20, sell_threshold=80)
stoch_signals = stoch_signal.generate_signals(btc)
```

#### 2. Combined Signals:
```python
# Simple Strategy (RSI + MACD)
simple_combined = CombinedSignal(
    signals=[rsi_signal, macd_signal],
    weights=[1.0, 1.0],
    quantity_threshold=2.0
)

# Complete Strategy (multiple signals)
full_strategy = CombinedSignal(
    signals=[rsi_signal, macd_signal, bb_signal, stoch_signal],
    weights=[1.0, 1.0, 0.8, 0.8],
    quantity_threshold=3.0,
    window=2
)

# Generate signals
simple_signals = simple_combined.generate_signals(btc)
full_signals = full_strategy.confirm_signals(btc)  # With confirmation
```

#### 3. Signal Analysis:
```python
# Count signals
buy_signals = (signals == -1).sum()
sell_signals = (signals == 1).sum()
neutral_signals = (signals == 0).sum()

print(f"Buy Signals: {buy_signals}")
print(f"Sell Signals: {sell_signals}")
print(f"Neutral Signals: {neutral_signals}")

# Last signal
last_signal = signals.iloc[-1]
if last_signal == -1:
    print("Last Signal: BUY")
elif last_signal == 1:
    print("Last Signal: SELL")
else:
    print("Last Signal: NEUTRAL")

# Last signal date
last_signal_date = signals[signals != 0].index[-1] if len(signals[signals != 0]) > 0 else None
if last_signal_date:
    print(f"Last Signal Date: {last_signal_date}")
```

---

## Visualizações / Visualizations

### Português:

#### 1. Gráfico Candlestick com Sinais:
```python
# Gráfico básico
ChartPlotter.plot_candlestick_with_signals(
    df=btc.get_prices(),
    title="BTC-USD - Análise Técnica",
    show_volume=True
)

# Gráfico com sinais
ChartPlotter.plot_candlestick_with_signals(
    df=btc.get_prices(),
    title="BTC-USD com Sinais de Trading",
    buy_signals=signals == -1,
    sell_signals=signals == 1,
    show_volume=True
)
```

#### 2. Gráfico de Indicadores:
```python
# Gráfico de RSI com sinais
ChartPlotter.plot_indicator_with_signals(
    price_data=btc.get_close_series(),
    indicator_data=rsi_values,
    title="BTC-USD com RSI",
    buy_signals=rsi_signals == -1,
    sell_signals=rsi_signals == 1,
    indicator_name="RSI (14)"
)

# Gráfico de MACD
ChartPlotter.plot_indicator_with_signals(
    price_data=btc.get_close_series(),
    indicator_data=macd_values['macd'],
    title="BTC-USD com MACD",
    buy_signals=macd_signals == 1,
    sell_signals=macd_signals == -1,
    indicator_name="MACD"
)
```

#### 3. Múltiplos Indicadores:
```python
# Gráfico com múltiplos indicadores
indicators_data = {
    'RSI': rsi_values,
    'MACD': macd_values['macd'],
    'Sharpe': sharpe_values,
    'Sortino': sortino_values
}

ChartPlotter.plot_multiple_indicators(
    data=indicators_data,
    title="BTC-USD - Indicadores Técnicos",
    subplot_titles=['RSI (14)', 'MACD', 'Sharpe Ratio', 'Sortino Ratio']
)
```

### English:

#### 1. Candlestick Chart with Signals:
```python
# Basic chart
ChartPlotter.plot_candlestick_with_signals(
    df=btc.get_prices(),
    title="BTC-USD - Technical Analysis",
    show_volume=True
)

# Chart with signals
ChartPlotter.plot_candlestick_with_signals(
    df=btc.get_prices(),
    title="BTC-USD with Trading Signals",
    buy_signals=signals == -1,
    sell_signals=signals == 1,
    show_volume=True
)
```

#### 2. Indicator Charts:
```python
# RSI chart with signals
ChartPlotter.plot_indicator_with_signals(
    price_data=btc.get_close_series(),
    indicator_data=rsi_values,
    title="BTC-USD with RSI",
    buy_signals=rsi_signals == -1,
    sell_signals=rsi_signals == 1,
    indicator_name="RSI (14)"
)

# MACD chart
ChartPlotter.plot_indicator_with_signals(
    price_data=btc.get_close_series(),
    indicator_data=macd_values['macd'],
    title="BTC-USD with MACD",
    buy_signals=macd_signals == 1,
    sell_signals=macd_signals == -1,
    indicator_name="MACD"
)
```

#### 3. Multiple Indicators:
```python
# Multiple indicators chart
indicators_data = {
    'RSI': rsi_values,
    'MACD': macd_values['macd'],
    'Sharpe': sharpe_values,
    'Sortino': sortino_values
}

ChartPlotter.plot_multiple_indicators(
    data=indicators_data,
    title="BTC-USD - Technical Indicators",
    subplot_titles=['RSI (14)', 'MACD', 'Sharpe Ratio', 'Sortino Ratio']
)
```

---

## Portfólio e Posições / Portfolio and Positions

### Português:

#### 1. Criar Portfólio:
```python
# Criar portfólio
portfolio = Portfolio("Meu Portfólio Cripto")

# Adicionar posições long
btc_position = LongPosition(asset=btc, quantity=0.5)
portfolio.add_position(btc_position)

eth_position = LongPosition(asset=eth, quantity=2.0)
portfolio.add_position(eth_position)

# Adicionar posição short
spy_short = ShortPosition(asset=spy, quantity=10)
portfolio.add_position(spy_short)

print(f"Total de posições: {len(portfolio.positions)}")
```

#### 2. Analisar Portfólio:
```python
# Valor total do portfólio
total_value = portfolio.total_value()
print(f"Valor Total: ${total_value:.2f}")

# P&L total
total_pnl = portfolio.total_pnl()
print(f"P&L Total: ${total_pnl:.2f}")

# Análise individual
for i, position in enumerate(portfolio.positions):
    position_value = position.total_value()
    position_pnl = position.calculate_pnl()
    print(f"Posição {i+1}: {position.asset.symbol}")
    print(f"  Valor: ${position_value:.2f}")
    print(f"  P&L: ${position_pnl:.2f}")
```

### English:

#### 1. Create Portfolio:
```python
# Create portfolio
portfolio = Portfolio("My Crypto Portfolio")

# Add long positions
btc_position = LongPosition(asset=btc, quantity=0.5)
portfolio.add_position(btc_position)

eth_position = LongPosition(asset=eth, quantity=2.0)
portfolio.add_position(eth_position)

# Add short position
spy_short = ShortPosition(asset=spy, quantity=10)
portfolio.add_position(spy_short)

print(f"Total positions: {len(portfolio.positions)}")
```

#### 2. Analyze Portfolio:
```python
# Total portfolio value
total_value = portfolio.total_value()
print(f"Total Value: ${total_value:.2f}")

# Total P&L
total_pnl = portfolio.total_pnl()
print(f"Total P&L: ${total_pnl:.2f}")

# Individual analysis
for i, position in enumerate(portfolio.positions):
    position_value = position.total_value()
    position_pnl = position.calculate_pnl()
    print(f"Position {i+1}: {position.asset.symbol}")
    print(f"  Value: ${position_value:.2f}")
    print(f"  P&L: ${position_pnl:.2f}")
```

---

## Exemplos Avançados / Advanced Examples

### Português:

#### 1. Sistema Completo de Trading:
```python
def complete_trading_system():
    # Configurar ativos
    assets_config = [
        ("BTC-USD", "Bitcoin"),
        ("ETH-USD", "Ethereum"),
        ("SPY", "S&P 500")
    ]

    results = {}

    for symbol, name in assets_config:
        # Criar asset
        provider = YahooProvider(period="1y", interval="1wk")
        asset = Crypto(symbol, provider=provider)

        # Calcular indicadores
        rsi = Rsi(period=14)
        macd = Macd()
        bb = BollingerBands(window=20, std_dev=2)

        # Criar sinais
        rsi_signal = RsiSignal(rsi=rsi, buy_threshold=30, sell_threshold=70)
        macd_signal = MacdSignal(macd=macd)
        bb_signal = BollingerBandsSignal(bb=bb)

        # Estratégia combinada
        strategy = CombinedSignal(
            signals=[rsi_signal, macd_signal, bb_signal],
            weights=[1.0, 1.0, 0.8],
            quantity_threshold=2.5
        )

        signals = strategy.confirm_signals(asset)

        # Análise
        current_price = asset.get_current_price()
        buy_count = (signals == -1).sum()
        sell_count = (signals == 1).sum()
        last_signal = signals.iloc[-1]

        results[symbol] = {
            'name': name,
            'price': current_price,
            'buy_signals': buy_count,
            'sell_signals': sell_count,
            'last_signal': 'BUY' if last_signal == -1 else 'SELL' if last_signal == 1 else 'NEUTRAL',
            'signals': signals
        }

        print(f"{name}: ${current_price:.2f} | Compras: {buy_count} | Vendas: {sell_count} | Último: {results[symbol]['last_signal']}")

    return results

# Executar sistema
results = complete_trading_system()
```

#### 2. Backtesting Simples:
```python
def simple_backtest(symbol, period="2y", interval="1wk"):
    # Configurar asset
    provider = YahooProvider(period=period, interval=interval)
    asset = Crypto(symbol, provider=provider)

    # Estratégia
    rsi = Rsi(period=14)
    macd = Macd()

    rsi_signal = RsiSignal(rsi=rsi, buy_threshold=25, sell_threshold=75)
    macd_signal = MacdSignal(macd=macd)

    strategy = CombinedSignal(
        signals=[rsi_signal, macd_signal],
        weights=[1.0, 1.0],
        quantity_threshold=2.0
    )

    signals = strategy.confirm_signals(asset)
    prices = asset.get_close_series()

    # Simular trades
    initial_capital = 10000
    capital = initial_capital
    position = 0
    trades = []

    for i, (date, signal) in enumerate(signals.items()):
        price = prices.iloc[i]

        if signal == -1 and position == 0:  # Buy
            shares = capital / price
            position = shares
            capital = 0
            trades.append({'date': date, 'type': 'BUY', 'price': price, 'shares': shares})

        elif signal == 1 and position > 0:  # Sell
            capital = position * price
            trades.append({'date': date, 'type': 'SELL', 'price': price, 'shares': position})
            position = 0

    # Resultados finais
    if position > 0:
        capital = position * prices.iloc[-1]

    total_return = (capital - initial_capital) / initial_capital * 100

    print(f"Backtesting {symbol}")
    print(f"Capital Inicial: ${initial_capital:.2f}")
    print(f"Capital Final: ${capital:.2f}")
    print(f"Retorno Total: {total_return:.2f}%")
    print(f"Número de Trades: {len(trades)}")

    return {
        'initial_capital': initial_capital,
        'final_capital': capital,
        'total_return': total_return,
        'trades': trades
    }

# Executar backtest
backtest_result = simple_backtest("BTC-USD")
```

### English:

#### 1. Complete Trading System:
```python
def complete_trading_system():
    # Setup assets
    assets_config = [
        ("BTC-USD", "Bitcoin"),
        ("ETH-USD", "Ethereum"),
        ("SPY", "S&P 500")
    ]

    results = {}

    for symbol, name in assets_config:
        # Create asset
        provider = YahooProvider(period="1y", interval="1wk")
        asset = Crypto(symbol, provider=provider)

        # Calculate indicators
        rsi = Rsi(period=14)
        macd = Macd()
        bb = BollingerBands(window=20, std_dev=2)

        # Create signals
        rsi_signal = RsiSignal(rsi=rsi, buy_threshold=30, sell_threshold=70)
        macd_signal = MacdSignal(macd=macd)
        bb_signal = BollingerBandsSignal(bb=bb)

        # Combined strategy
        strategy = CombinedSignal(
            signals=[rsi_signal, macd_signal, bb_signal],
            weights=[1.0, 1.0, 0.8],
            quantity_threshold=2.5
        )

        signals = strategy.confirm_signals(asset)

        # Analysis
        current_price = asset.get_current_price()
        buy_count = (signals == -1).sum()
        sell_count = (signals == 1).sum()
        last_signal = signals.iloc[-1]

        results[symbol] = {
            'name': name,
            'price': current_price,
            'buy_signals': buy_count,
            'sell_signals': sell_count,
            'last_signal': 'BUY' if last_signal == -1 else 'SELL' if last_signal == 1 else 'NEUTRAL',
            'signals': signals
        }

        print(f"{name}: ${current_price:.2f} | Buys: {buy_count} | Sells: {sell_count} | Last: {results[symbol]['last_signal']}")

    return results

# Run system
results = complete_trading_system()
```

#### 2. Simple Backtesting:
```python
def simple_backtest(symbol, period="2y", interval="1wk"):
    # Setup asset
    provider = YahooProvider(period=period, interval=interval)
    asset = Crypto(symbol, provider=provider)

    # Strategy
    rsi = Rsi(period=14)
    macd = Macd()

    rsi_signal = RsiSignal(rsi=rsi, buy_threshold=25, sell_threshold=75)
    macd_signal = MacdSignal(macd=macd)

    strategy = CombinedSignal(
        signals=[rsi_signal, macd_signal],
        weights=[1.0, 1.0],
        quantity_threshold=2.0
    )

    signals = strategy.confirm_signals(asset)
    prices = asset.get_close_series()

    # Simulate trades
    initial_capital = 10000
    capital = initial_capital
    position = 0
    trades = []

    for i, (date, signal) in enumerate(signals.items()):
        price = prices.iloc[i]

        if signal == -1 and position == 0:  # Buy
            shares = capital / price
            position = shares
            capital = 0
            trades.append({'date': date, 'type': 'BUY', 'price': price, 'shares': shares})

        elif signal == 1 and position > 0:  # Sell
            capital = position * price
            trades.append({'date': date, 'type': 'SELL', 'price': price, 'shares': position})
            position = 0

    # Final results
    if position > 0:
        capital = position * prices.iloc[-1]

    total_return = (capital - initial_capital) / initial_capital * 100

    print(f"Backtesting {symbol}")
    print(f"Initial Capital: ${initial_capital:.2f}")
    print(f"Final Capital: ${capital:.2f}")
    print(f"Total Return: {total_return:.2f}%")
    print(f"Number of Trades: {len(trades)}")

    return {
        'initial_capital': initial_capital,
        'final_capital': capital,
        'total_return': total_return,
        'trades': trades
    }

# Run backtest
backtest_result = simple_backtest("BTC-USD")
```

---

## Dicas e Melhores Práticas / Tips and Best Practices

### Português:

1. **Períodos e Intervalos:** Use períodos mais longos (1y, 2y) para análise de tendências e intervalos semanais (1wk) para reduzir ruído

2. **Combinação de Sinais:** Combine múltiplos indicadores para sinais mais robustos

3. **Validação:** Sempre teste estratégias com dados históricos antes de usar em tempo real

4. **Gerenciamento de Risco:** Use indicadores de risco (Sharpe, Sortino) para avaliar estratégias

5. **Visualização:** Use gráficos para validar sinais visualmente

### English:

1. **Periods and Intervals:** Use longer periods (1y, 2y) for trend analysis and weekly intervals (1wk) to reduce noise

2. **Signal Combination:** Combine multiple indicators for more robust signals

3. **Validation:** Always test strategies with historical data before real-time use

4. **Risk Management:** Use risk indicators (Sharpe, Sortino) to evaluate strategies

5. **Visualization:** Use charts to visually validate signals

---

## Suporte e Troubleshooting / Support and Troubleshooting

### Português:

- **Erro de importação:** Verifique se o ambiente virtual está ativado
- **Dados não carregam:** Verifique conexão com internet e símbolo do ativo
- **Gráficos não aparecem:** Instale dependências adicionais: `pip install plotly`

### English:

- **Import error:** Check if virtual environment is activated
- **Data not loading:** Check internet connection and asset symbol
- **Charts not showing:** Install additional dependencies: `pip install plotly`

---

**Sistema Market Montrezor - Versão 1.0**
**Desenvolvido para análise técnica completa de mercados financeiros**
