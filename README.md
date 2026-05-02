# 🚀 MARKET ANALYZER - Crypto Gems System

**Advanced cryptocurrency analysis system specialized in finding low market cap gems with high potential.**

---

## 🇺🇸 English

### 📋 Overview
MARKET ANALYZER is a sophisticated cryptocurrency analysis platform designed to identify promising low market cap tokens (gems) with significant growth potential. The system combines technical analysis, social intelligence, and multi-timeframe persistence tracking to provide comprehensive market insights.

### ✨ Key Features
- **Multi-Timeframe Analysis**: Tracks gems across 3, 7, and 14-day persistence periods
- **Social Intelligence**: Real-time YouTube API and Telegram scraping for sentiment analysis
- **Technical Scoring**: Advanced quantitative and social scoring algorithms
- **Interactive Dashboard**: Plotly-based visualization with comprehensive metrics
- **Smart Filtering**: Zone-based classification (Early Accumulation, Strong, Breakout)
- **Persistence Tracking**: Cumulative counters for consistent performers
- **Leader Identification**: Automated detection of confirmed market leaders

### �️ Tech Stack
- **Python 3.12+** with pandas, plotly, requests
- **Data Sources**: CoinMarketCap API, YouTube API, Telegram scraping
- **Storage**: CSV snapshots + JSON daily data
- **Visualization**: Interactive Plotly dashboards
- **Caching**: 12-hour intelligent cache system

### 🚀 Quick Start
```bash
# Clone and setup
git clone https://github.com/igormontrezor/market-analyzer-crypto-gems.git
cd market-analyzer-crypto-gems/gems_system

# Run analysis
python gems_finder.py

# View results
python visualizer.py
```

---

## 🇧🇷 Português

### 📋 Visão Geral
MARKET ANALYZER é uma plataforma sofisticada de análise de criptomoedas projetada para identificar tokens de baixa capitalização (gems) com significativo potencial de crescimento. O sistema combina análise técnica, inteligência social e rastreamento de persistência multi-timeframe para fornecer insights completos do mercado.

### ✨ Recursos Principais
- **Análise Multi-Timeframe**: Rastreia gems em períodos de persistência de 3, 7 e 14 dias
- **Inteligência Social**: API YouTube e scraping Telegram em tempo real para análise de sentimento
- **Scoring Técnico**: Algoritmos avançados de scoring quantitativo e social
- **Dashboard Interativo**: Visualização baseada em Plotly com métricas completas
- **Filtragem Inteligente**: Classificação baseada em zonas (Early Accumulation, Strong, Breakout)
- **Rastreamento de Persistência**: Contadores cumulativos para performers consistentes
- **Identificação de Líderes**: Detecção automatizada de líderes confirmados de mercado

### 🛠️ Stack Tecnológico
- **Python 3.12+** com pandas, plotly, requests
- **Fontes de Dados**: CoinMarketCap API, YouTube API, scraping Telegram
- **Armazenamento**: Snapshots CSV + dados diários JSON
- **Visualização**: Dashboards interativos Plotly
- **Cache**: Sistema inteligente de cache de 12 horas

### 🚀 Início Rápido
```bash
# Clonar e configurar
git clone https://github.com/igormontrezor/market-analyzer-crypto-gems.git
cd market-analyzer-crypto-gems/gems_system

# Executar análise
python gems_finder.py

# Visualizar resultados
python visualizer.py
```

---

## � Project Structure

```
market-analyzer-crypto-gems/
├── gems_system/              # Main analysis system
│   ├── gems_finder.py        # Core analysis engine
│   ├── visualizer.py         # Interactive dashboard
│   ├── persistence_tracker.py # Persistence tracking
│   ├── social_analyzer_yt_telegram.py  # Social intelligence
│   ├── data/                 # Data storage
│   │   ├── snapshots/        # CSV analysis files
│   │   └── daily_snapshots/  # JSON daily data
│   └── guide/                # Documentation
├── analysis_system/          # Technical analysis module
├── config/                   # Configuration files
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12+
- CoinMarketCap API key
- YouTube API key (optional)

### Quick Setup
```bash
# Clone repository
git clone https://github.com/igormontrezor/market-analyzer-crypto-gems.git
cd market-analyzer-crypto-gems

# Create virtual environment
python -m venv .venv

# Activate environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
```bash
# Set API keys
# Windows
set CMC_API_KEY=your_key_here
set YOUTUBE_API_KEY=your_key_here

# Linux/Mac
export CMC_API_KEY=your_key_here
export YOUTUBE_API_KEY=your_key_here
```

## 🎯 System Features

### 🧠 **Social Intelligence**
- **YouTube API**: Real-time sentiment analysis with accurate search
- **Telegram Scraping**: Channel analysis with intelligent weighting
- **Social Validation**: Combined with technical signals for accuracy
- **Velocity Metrics**: YouTube engagement + Telegram activity tracking

### 📊 **Technical Analysis**
- **Multi-Timeframe**: 3, 7, 14-day persistence tracking
- **Zone Classification**: Early Accumulation, Strong, Breakout detection
- **Scoring Algorithm**: Quantitative + social composite scoring
- **Leader Detection**: Automated market leader identification

### 📊 **Multi-Timeframe Analysis**
- **Short Term**: 1 dia (spikes e momentum)
- **Medium Term**: 3-7 dias (persistência e recuperação)
- **Long Term**: 7-14 dias (tendência e consistência)

### 🎯 **8 Camadas Inteligentes**
1. **Volume Real** (3 zonas: Breakout, Strong, Accumulation)
2. **Persistência Multi-Timeframe** (3, 7, 14 dias)
3. **Estrutura Técnica** (price resilience, supply risk)
4. **Social Validation** (YouTube + Telegram filtrado)

### 📈 **Faixas de Busca**
- **50M-30M**: Criptomoedas de médio porte
- **20M-10M**: Criptomoedas de pequeno porte
- **Cache**: 12 horas (otimizado para social validation)

---

## 📊 **Analysis System Features**

### 🔧 **Indicadores Técnicos**
- **Momentum**: RSI, Stochastic RSI, MACD
- **Volatilidade**: Bollinger Bands
- **Médias Móveis**: SMA, EMA
- **Risco**: Sharpe Ratio, Sortino Ratio

### 📈 **Sinais de Trading**
- **RSI Signal**: Baseado em overbought/oversold
- **MACD Signal**: Baseado em cruzamentos
- **Bollinger Bands Signal**: Baseado nas bandas
- **Combined Signal**: Combinação ponderada

---

## 📁 **Estrutura do Projeto**

```
market-system-montrezor/
├── gems_system/                    # 🚀 GEMS Finder v3.1
│   ├── gems_finder.py             # Busca inteligente de gems
│   ├── social_analyzer_yt_telegram.py # Social validation
│   ├── config.py                  # Configurações
│   ├── run.bat / run.ps1         # Scripts de execução
│   └── data/
│       ├── snapshots/             # Histórico CSV
│       ├── daily_snapshots/       # Snapshots diários JSON
│       └── gems_cache.json        # Cache 12h
├── analysis_system/               # 📊 Análise técnica
│   ├── indicators/                # Indicadores técnicos
│   ├── signals/                   # Sinais de trading
│   ├── strategies/                # Estratégias
│   └── trading/                   # Métodos e checklists
├── config/                        # 🔧 Configurações globais
└── simple_crypto_list_yfinance.py # Lista de criptomoedas
```

---

## 🎯 **Como Usar**

### 💎 **GEMS Finder**
```bash
# Executar busca completa
cd gems_system
python gems_finder.py

# Resultados salvos em:
# - data/snapshots/gems_consolidated_TIMESTAMP.csv
# - data/snapshots/gems_50m_range_TIMESTAMP.csv
# - data/snapshots/gems_10m_range_TIMESTAMP.csv
```

### 📊 **Analysis System**
```python
# Exemplo de uso
from analysis_system import Crypto, YahooProvider, Rsi, ChartPlotter

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
    title="BTC-USD - RSI Analysis"
)
```

---

## 📋 **Resultados e Saídas**

### 💎 **GEMS Finder Output**
- **CSV Completo**: Todas as gems com análise completa
- **Social Analysis**: Gems com validação social marcadas
- **Timeframe Analysis**: Persistência em 3, 7, 14 dias
- **Cache Inteligente**: 12h de duração

### 📊 **Analysis System Output**
- **Gráficos Interativos**: Candlestick com indicadores
- **Sinais de Trading**: Buy/Sell automatizados
- **Relatórios**: Métricas de performance
- **Backtesting**: Validação de estratégias

---

## 🔧 **Configuração**

### 📝 **API Keys**
```python
# config/keys_template.py
YOUTUBE_API_KEY = "sua_chave_aqui"
COINGECKO_API_KEY = "sua_chave_aqui"
```

### ⚙️ **Parâmetros GEMS**
```python
# gems_system/config.py
SOCIAL_CACHE_HOURS = 1
SOCIAL_ANALYSIS_MIN_RATIO = 0.7
SOCIAL_ANALYSIS_MIN_DAYS = 2
```

---

## 🚀 **Social Validation**

### 📺 **YouTube Analysis**
- **Query**: Nomes completos CoinGecko
- **Velocity**: Vídeos hoje vs média 7 dias
- **Keywords**: Contextuais para cada moeda

### 📱 **Telegram Analysis**
- **Canais**: 4 canais principais com pesos
- **Weights**: cryptochat (1.0), crypto_signals (0.5), etc.
- **Spike**: Menções hoje vs média 7 dias

### 🎯 **Validação Combinada**
- **EXPLOSÃO SOCIAL**: YouTube > 2x E Telegram > 2x
- **ATENÇÃO FORTE**: YouTube > 1.5x E Telegram > 1.5x
- **ATENÇÃO MODERADA**: YouTube > 1.2x E Telegram > 1.2x

---

## 📈 **Exemplos de Uso**

### 💎 **Buscar Gems com Social Validation**
```python
from gems_system import GemsFinder

finder = GemsFinder()
gems = finder.find_gems_by_ranges([
    {"min_mc": 30000000, "max_mc": 50000000},
    {"min_mc": 10000000, "max_mc": 20000000}
])

# Gems com social forte marcadas no CSV
```

### 📊 **Análise Técnica Completa**
```bash
# Análise completa com todos os indicadores
python analysis_system/main.py --symbol BTC-USD --plot-all-indicators

# Estratégia combinada
python analysis_system/main.py --symbol ETH-USD --strategy combined
```

---

## 🔄 **Cache e Performance**

### 💾 **Cache System**
- **Duração**: 12 horas (otimizado)
- **Economia**: 50% menos requisições API
- **Persistência**: Dados mantidos entre execuções
- **Social**: Funciona com cache de 12h

### 📊 **Snapshots**
- **Histórico**: Todos os resultados salvos
- **Daily**: Resumo diário em JSON
- **CSV**: Dados completos por faixa
- **Consolidated**: Todos os dados em um arquivo

---

## 🎯 **Melhorias v3.1**

### ✅ **Implementadas**
- **Cache otimizado**: 12h para social validation
- **Social funcionando**: persistence_days >= 2
- **Gems marcadas**: Social forte no CSV
- **Sistema profissional**: 100% funcional

### 🚀 **Próximas**
- **Mais faixas**: Expansão para outros ranges
- **APIs adicionais**: Reddit, Twitter
- **Machine Learning**: Previsões avançadas
- **Dashboard**: Interface web

---

## 🤝 **Contribuindo**

1. Fork do repositório
2. Criar branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit (`git commit -m 'Adicionar nova funcionalidade'`)
4. Push (`git push origin feature/nova-funcionalidade`)
5. Pull Request

---

## 📄 **Licença**

Este projeto está licenciado sob a Licença MIT.

---

## 🏆 **Status do Sistema**

✅ **GEMS System**: 100% funcional
✅ **Social Validation**: Ativa e funcionando
✅ **Cache**: Otimizado para 12h
✅ **Scripts**: .bat e .ps1 prontos
✅ **Documentação**: Completa e atualizada

**🚀 Sistema pronto para produção!**
