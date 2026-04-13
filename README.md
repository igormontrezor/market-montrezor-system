# Market Montrezor System

A comprehensive financial market analysis system with technical indicators, trading signals, and advanced visualizations.

## Features

- **Technical Indicators**: RSI, MACD, Bollinger Bands, SMA, EMA, Stochastic RSI, Sharpe Ratio, Sortino Ratio
- **Trading Signals**: Automated buy/sell signals with customizable thresholds
- **Advanced Plotting**: Interactive charts with candlestick, volume, and signal overlays
- **Portfolio Management**: Track multiple assets and positions
- **Modular Architecture**: Clean, extensible codebase
- **Command Line Interface**: Easy-to-use CLI for analysis and plotting

## Installation

```bash
# Clone the repository
git clone https://github.com/igormontrezor/market-system-montrezor.git
cd market-system-montrezor

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Basic Analysis
```bash
# Simple analysis with plotting
python src/market_analyze/main.py --symbol BTC-USD --period 6mo --interval 1wk --plot

# Plot specific indicators
python src/market_analyze/main.py --symbol BTC-USD --plot-rsi
python src/market_analyze/main.py --symbol BTC-USD --plot-macd
python src/market_analyze/main.py --symbol BTC-USD --plot-bb
python src/market_analyze/main.py --symbol BTC-USD --plot-all-indicators
```

### Programmatic Usage
```python
from market_analyze import Crypto, YahooProvider, Rsi, ChartPlotter

# Create asset
provider = YahooProvider(period="6mo", interval="1wk")
btc = Crypto("BTC-USD", provider=provider)

# Calculate RSI
rsi = Rsi(period=14)
rsi_values = rsi.calculate(btc)

# Plot with signals
ChartPlotter.plot_indicator_with_signals(
    price_data=btc.get_close_series(),
    indicator_data=rsi_values,
    title="BTC-USD - RSI Analysis"
)
```

## Available Commands

| Command | Description |
|---------|-------------|
| `--symbol SYMBOL` | Asset symbol (default: BTC-USD) |
| `--period PERIOD` | Data period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max |
| `--interval INTERVAL` | Data interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo |
| `--plot` | Show candlestick chart with signals |
| `--plot-rsi` | Plot RSI indicator with signals |
| `--plot-macd` | Plot MACD indicator with signals |
| `--plot-bb` | Plot Bollinger Bands |
| `--plot-sharpe` | Plot Sharpe Ratio |
| `--plot-sortino` | Plot Sortino Ratio |
| `--plot-all-indicators` | Plot complete indicators panel |

## Examples

### 1. Complete Analysis with All Signals
```bash
python src/market_analyze/main.py --symbol ETH-USD --period 1y --interval 1d --plot
```

### 2. RSI Analysis Only
```bash
python src/market_analyze/main.py --symbol SPY --period 6mo --plot-rsi
```

### 3. Multiple Assets Comparison
```python
from market_analyze import Crypto, YahooProvider, ChartPlotter

assets = ['BTC-USD', 'ETH-USD', 'SPY']
data = {}

for symbol in assets:
    provider = YahooProvider(period="6mo", interval="1wk")
    asset = Crypto(symbol, provider=provider)
    data[symbol] = asset.get_close_series()

ChartPlotter.plot_multiple_indicators(
    data=data,
    title="Cryptocurrencies vs Stocks Comparison"
)
```

### 4. Custom Strategy
```python
from market_analyze import *
from market_analyze.signals import CombinedSignal

# Setup assets
provider = YahooProvider(period="1y", interval="1wk")
btc = Crypto("BTC-USD", provider=provider)

# Create indicators
rsi = Rsi(period=14)
macd = Macd()
bb = BollingerBands(window=20, std_dev=2)

# Create signals
rsi_signal = RsiSignal(rsi=rsi, buy_threshold=30, sell_threshold=70)
macd_signal = MacdSignal(macd=macd)
bb_signal = BollingerBandsSignal(bb=bb)

# Combine signals
strategy = CombinedSignal(
    signals=[rsi_signal, macd_signal, bb_signal],
    weights=[1.0, 1.0, 0.8],
    quantity_threshold=2.0
)

# Generate signals
signals = strategy.generate_signals(btc)

# Plot results
ChartPlotter.plot_candlestick_with_signals(
    df=btc.get_prices(),
    title="BTC-USD - Combined Strategy",
    buy_signals=signals == -1,
    sell_signals=signals == 1,
    show_volume=True
)
```

## Project Structure

```
market-system-montrezor/
|
src/
|-- market_analyze/
|   |-- __init__.py
|   |-- main.py                    # CLI entry point
|   |-- assets/
|   |   |-- __init__.py
|   |   |-- asset.py               # Asset, Crypto, Portfolio classes
|   |-- indicators/
|   |   |-- __init__.py
|   |   |-- indicators.py          # All technical indicators
|   |-- signals/
|   |   |-- __init__.py
|   |   |-- signals.py             # Trading signal classes
|   |-- plotting/
|   |   |-- __init__.py
|   |   |-- charts.py              # Chart plotting functionality
|   |-- examples/
|   |   |-- basic_usage.py         # Basic usage examples
|   |   |-- strategy_analysis.py   # Advanced strategy examples
|
notebooks/                          # Jupyter notebooks
docs/                              # Documentation
tests/                             # Unit tests
```

## Available Indicators

- **Moving Averages**: SMA, EMA
- **Momentum**: RSI, Stochastic RSI, MACD
- **Volatility**: Bollinger Bands
- **Risk Metrics**: Sharpe Ratio, Sortino Ratio

## Available Signals

- **RSI Signal**: Based on overbought/oversold levels
- **MACD Signal**: Based on MACD crossovers
- **Bollinger Bands Signal**: Based on price touching bands
- **Combined Signal**: Weighted combination of multiple signals

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

# Sistema Market Montrezor

Sistema completo para análise de mercado financeiro com indicadores técnicos, sinais de trading e visualizações.

## Características

- **Indicadores Técnicos**: RSI, MACD, Bollinger Bands, SMA, EMA, Stochastic RSI, Sharpe Ratio, Sortino Ratio
- **Sinais de Trading**: Sinais automáticos de compra/venda com limiares personalizáveis
- **Visualizações Avançadas**: Gráficos interativos com candlestick, volume e sobreposição de sinais
- **Gestão de Portfólio**: Acompanhe múltiplos ativos e posições
- **Arquitetura Modular**: Código limpo e extensível
- **Interface de Linha de Comando**: CLI fácil de usar para análise e plotagem

## Instalação

```bash
# Clonar repositório
git clone https://github.com/igormontrezor/market-system-montrezor.git
cd market-system-montrezor

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## Início Rápido

### Análise Básica
```bash
# Análise simples com plotagem
python src/market_analyze/main.py --symbol BTC-USD --period 6mo --interval 1wk --plot

# Plotar indicadores específicos
python src/market_analyze/main.py --symbol BTC-USD --plot-rsi
python src/market_analyze/main.py --symbol BTC-USD --plot-macd
python src/market_analyze/main.py --symbol BTC-USD --plot-bb
python src/market_analyze/main.py --symbol BTC-USD --plot-all-indicators
```

### Uso Programático
```python
from market_analyze import Crypto, YahooProvider, Rsi, ChartPlotter

# Criar ativo
provider = YahooProvider(period="6mo", interval="1wk")
btc = Crypto("BTC-USD", provider=provider)

# Calcular RSI
rsi = Rsi(period=14)
rsi_values = rsi.calculate(btc)

# Plotar com sinais
ChartPlotter.plot_indicator_with_signals(
    price_data=btc.get_close_series(),
    indicator_data=rsi_values,
    title="BTC-USD - Análise RSI"
)
```

## Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `--symbol SYMBOL` | Símbolo do ativo (padrão: BTC-USD) |
| `--period PERIOD` | Período dos dados: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max |
| `--interval INTERVAL` | Intervalo dos dados: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo |
| `--plot` | Mostrar gráfico candlestick com sinais |
| `--plot-rsi` | Plotar indicador RSI com sinais |
| `--plot-macd` | Plotar indicador MACD com sinais |
| `--plot-bb` | Plotar Bollinger Bands |
| `--plot-sharpe` | Plotar Sharpe Ratio |
| `--plot-sortino` | Plotar Sortino Ratio |
| `--plot-all-indicators` | Plotar painel completo de indicadores |

## Exemplos

### 1. Análise Completa com Todos os Sinais
```bash
python src/market_analyze/main.py --symbol ETH-USD --period 1y --interval 1d --plot
```

### 2. Análise Apenas de RSI
```bash
python src/market_analyze/main.py --symbol SPY --period 6mo --plot-rsi
```

### 3. Comparação de Múltiplos Ativos
```python
from market_analyze import Crypto, YahooProvider, ChartPlotter

assets = ['BTC-USD', 'ETH-USD', 'SPY']
data = {}

for symbol in assets:
    provider = YahooProvider(period="6mo", interval="1wk")
    asset = Crypto(symbol, provider=provider)
    data[symbol] = asset.get_close_series()

ChartPlotter.plot_multiple_indicators(
    data=data,
    title="Comparação Criptomoedas vs Ações"
)
```

### 4. Estratégia Personalizada
```python
from market_analyze import *
from market_analyze.signals import CombinedSignal

# Configurar ativos
provider = YahooProvider(period="1y", interval="1wk")
btc = Crypto("BTC-USD", provider=provider)

# Criar indicadores
rsi = Rsi(period=14)
macd = Macd()
bb = BollingerBands(window=20, std_dev=2)

# Criar sinais
rsi_signal = RsiSignal(rsi=rsi, buy_threshold=30, sell_threshold=70)
macd_signal = MacdSignal(macd=macd)
bb_signal = BollingerBandsSignal(bb=bb)

# Combinar sinais
strategy = CombinedSignal(
    signals=[rsi_signal, macd_signal, bb_signal],
    weights=[1.0, 1.0, 0.8],
    quantity_threshold=2.0
)

# Gerar sinais
signals = strategy.generate_signals(btc)

# Plotar resultados
ChartPlotter.plot_candlestick_with_signals(
    df=btc.get_prices(),
    title="BTC-USD - Estratégia Combinada",
    buy_signals=signals == -1,
    sell_signals=signals == 1,
    show_volume=True
)
```

## Estrutura do Projeto

```
market-system-montrezor/
|
src/
|-- market_analyze/
|   |-- __init__.py
|   |-- main.py                    # Ponto de entrada CLI
|   |-- assets/
|   |   |-- __init__.py
|   |   |-- asset.py               # Classes Asset, Crypto, Portfolio
|   |-- indicators/
|   |   |-- __init__.py
|   |   |-- indicators.py          # Todos os indicadores técnicos
|   |-- signals/
|   |   |-- __init__.py
|   |   |-- signals.py             # Classes de sinais de trading
|   |-- plotting/
|   |   |-- __init__.py
|   |   |-- charts.py              # Funcionalidade de plotagem de gráficos
|   |-- examples/
|   |   |-- basic_usage.py         # Exemplos de uso básico
|   |   |-- strategy_analysis.py   # Exemplos avançados de estratégia
|
notebooks/                          # Jupyter notebooks
docs/                              # Documentação
tests/                             # Testes unitários
```

## Indicadores Disponíveis

- **Médias Móveis**: SMA, EMA
- **Momentum**: RSI, Stochastic RSI, MACD
- **Volatilidade**: Bollinger Bands
- **Métricas de Risco**: Sharpe Ratio, Sortino Ratio

## Sinais Disponíveis

- **Sinal RSI**: Baseado em níveis de sobrecompra/sobrevenda
- **Sinal MACD**: Baseado em cruzamentos MACD
- **Sinal Bollinger Bands**: Baseado no preço tocando as bandas
- **Sinal Combinado**: Combinação ponderada de múltiplos sinais

## Contribuindo

1. Fork do repositório
2. Criar branch de feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit das mudanças (`git commit -m 'Adicionar nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abrir Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.
