# Market Montrezor System v3.1

🚀 **Sistema avançado de análise de mercado com GEMS Finder e Social Intelligence**

---

## 🎯 **Visão Geral**

Sistema completo para análise de mercado financeiro com duas principais funcionalidades:

### 💎 **GEMS System v3.1**
- **GEMS Finder**: Identificação de criptomoedas de alto potencial
- **Social Validation**: Análise social inteligente (YouTube + Telegram)
- **Multi-Timeframe**: Análise em 3, 7 e 14 dias
- **Cache Otimizado**: 12 horas para economia de API

### 📊 **Analysis System**
- **Indicadores Técnicos**: RSI, MACD, Bollinger Bands, SMA, EMA
- **Sinais de Trading**: Automatizados com limiares personalizáveis
- **Visualizações Avançadas**: Gráficos interativos e candlestick
- **Gestão de Portfólio**: Acompanhamento múltiplos ativos

---

## 🚀 **Quick Start - GEMS System**

### Instalação
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

### Executar GEMS Finder
```bash
# Windows Batch
cd gems_system
run.bat

# Windows PowerShell
cd gems_system
run.ps1

# Python direto
cd gems_system
python gems_finder.py
```

---

## 💎 **GEMS System Features**

### 🧠 **Social Intelligence**
- **YouTube API**: Análise com nomes completos (sem falsos positivos)
- **Telegram**: Canais com pesos inteligentes (sem spam/pump)
- **Validação Social**: Só analisa com sinais técnicos fortes
- **Métricas**: YouTube Velocity + Telegram Spike

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
