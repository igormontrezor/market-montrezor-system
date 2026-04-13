# Market Montrezor System

Sistema completo para análise de mercado financeiro com indicadores técnicos, sinais de trading e visualizações.

## Estrutura do Projeto

```
market_montrezor_system/
|
src/
|-- market_analyze/
|   |-- __init__.py
|   |-- main.py
|   |-- assets/
|   |   |-- __init__.py
|   |   |-- asset.py          # Asset, Crypto, Btc
|   |   |-- portfolio.py      # Portfolio, Position, LongPosition, ShortPosition
|   |   |-- provider.py       # Provider, YahooProvider
|   |-- indicators/
|   |   |-- __init__.py
|   |   |-- indicators.py     # SMA, EMA, RSI, StochRSI, BB, MACD, Sharpe, Sortino
|   |   |-- calculations.py   # Calculations class
|   |-- signals/
|   |   |-- __init__.py
|   |   |-- signals.py        # Signal classes e CombinedSignal
|   |-- plotting/
|   |   |-- __init__.py
|   |   |-- charts.py         # ChartPlotter class
|   |-- examples/
|   |   |-- __init__.py
|   |   |-- basic_usage.py    # Exemplo básico
|   |   |-- strategy_analysis.py # Análise avançada
|   |-- data/                 # Para futuros módulos de dados
|
notebooks/
|-- market_analysis_oop.ipynb  # Notebook original (não modificado)
```

## Instalação

1. Criar ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Instalar dependências:
```bash
pip install pandas numpy yfinance matplotlib plotly seaborn
```

## Como Usar

### 1. Análise Simples via Linha de Comando

```bash
cd src/market_analyze
python main.py --symbol BTC-USD --period 1y --interval 1wk --plot
```

### 2. Exemplos

#### Exemplo Básico
```bash
python main.py --example basic
```

#### Análise de Estratégia
```bash
python main.py --example strategy
```

### 3. Uso Programático

```python
from market_analyze import Crypto, YahooProvider, Rsi, RsiSignal, ChartPlotter

# Criar asset
provider = YahooProvider(period="1y", interval="1wk")
btc = Crypto("BTC-USD", provider=provider)

# Calcular RSI
rsi = Rsi(period=14)
btc_rsi = rsi.calculate(btc)

# Gerar sinais
rsi_signal = RsiSignal(rsi=rsi, buy_threshold=30, sell_threshold=70)
signals = rsi_signal.generate_signals(btc)

# Plotar
ChartPlotter.plot_indicator_with_signals(
    price_data=btc.get_prices()['Close'],
    indicator_data=btc_rsi,
    title="BTC-USD com RSI",
    buy_signals=signals == -1,
    sell_signals=signals == 1,
    indicator_name="RSI (14)"
)
```

## Classes Principais

### Assets
- **Asset**: Classe base abstrata para ativos
- **Crypto**: Implementação para criptomoedas
- **Portfolio**: Gerencia portfólio de posições
- **Position**: Posições long/short

### Providers
- **YahooProvider**: Obtém dados do Yahoo Finance

### Indicadores Técnicos
- **SimpleMovingAverage**: Média móvel simples
- **ExponentialMovingAverage**: Média móvel exponencial
- **Rsi**: Relative Strength Index
- **StochRsi**: Stochastic RSI
- **BollingerBands**: Bandas de Bollinger
- **Macd**: MACD
- **SharpeRatio**: Índice de Sharpe
- **SortinoRatio**: Índice de Sortino

### Sinais
- **RsiSignal**: Sinais baseados em RSI
- **StochRsiSignal**: Sinais baseados em StochRSI
- **BollingerBandsSignal**: Sinais baseados em Bandas de Bollinger
- **MacdSignal**: Sinais baseados em MACD
- **CombinedSignal**: Combina múltiplos sinais

### Visualização
- **ChartPlotter**: Classe para criar gráficos interativos

## Funcionalidades

- Indicadores técnicos completos
- Sinais de trading configuráveis
- Combinação de estratégias
- Visualizações interativas com Plotly
- Suporte para múltiplos timeframes
- Análise de risco (Sharpe, Sortino)

## Exemplos de Uso

Verifique os arquivos em `examples/` para exemplos detalhados:

- `basic_usage.py`: Exemplo básico de uso
- `strategy_analysis.py`: Análise avançada de estratégias

## Comando de Ajuda

```bash
python main.py --help
```

## Notas

- O notebook original `market_analysis_oop.ipynb` não foi modificado
- Todo o código foi reestruturado em módulos organizados
- O sistema mantém a mesma funcionalidade do notebook original
- Adicionadas novas funcionalidades de visualização e organização
