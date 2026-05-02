# 🚀 GEMS SYSTEM - Guia Completo | Complete Guide

## 🇧🇷 Português

### 📋 O que é o GEMS SYSTEM?
Sistema automatizado para buscar e analisar criptomoedas de baixo market cap (gems) com alto potencial de retorno.

### 🛠️ Pré-requisitos
1. Python 3.8+
2. Ambiente virtual ativado (`venv`)
3. API Key da CoinMarketCap (opcional, aumenta limites)

### 📦 Instalação e Configuração

#### 1. Ativar ambiente virtual
```bash
cd c:\market_montrezor_system
.venv\Scripts\activate
```

#### 2. Instalar dependências
```bash
pip install requests pandas numpy
```

#### 3. Configurar API Key (opcional)
```bash
# Windows
set CMC_API_KEY=sua_chave_aqui
```

### 🚀 Como Usar

#### Método 1: Execução Direta (Recomendado)
```bash
cd gems_system
python gems_finder.py
```

#### Método 2: Via Batch/PowerShell
```bash
# Windows
run.bat
# ou
run.ps1
```

#### Método 3: Em Notebook Jupyter
```python
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from gems_finder import find_gems_by_ranges

# Buscar por faixas
coins, df = find_gems_by_ranges()
print(df.head(10))
```

### 📊 Entendendo os Resultados

#### Colunas Principais
- **symbol**: Símbolo da moeda
- **name**: Nome completo
- **market_cap**: Market Cap atual
- **volume**: Volume 24h
- **vol_mc_ratio**: Volume / Market Cap (liquidez)
- **final_score**: Score composto (0-10)

#### Faixas Buscadas
- **50m_range**: MC $40M-$60M, Volume >$500K
- **10m_range**: MC $8M-$15M, Volume >$200K

### 💾 Arquivos Gerados

#### Estrutura
```
data/
├── gems_today.csv           # Última execução
├── gems_YYYYMMDD.csv       # Snapshot diário
└── snapshots/
    ├── gems_50m_range_*.csv # Faixa 50M
    ├── gems_10m_range_*.csv # Faixa 10M
    └── gems_consolidated_*.csv # Todas as gems
```

### 🎯 Melhores Práticas

#### 1. Análise Diária
```python
# Ver gems de hoje
import pandas as pd
df = pd.read_csv('data/gems_today.csv')

# Filtrar gems com bom score
high_score = df[df['final_score'] > 7]
print(high_score.sort_values('final_score', ascending=False))
```

#### 2. Comparação Histórica
```python
# Comparar hoje vs ontem
today = pd.read_csv('data/gems_20260501.csv')
yesterday = pd.read_csv('data/gems_20260430.csv')

# Novas entradas
new_gems = today[~today['symbol'].isin(yesterday['symbol'])]
print(f"Novas gems: {len(new_gems)}")
```

#### 3. Análise por Faixa
```python
# Analisar faixa 50M
df_50m = pd.read_csv('data/snapshots/gems_50m_range_*.csv')
top_liquidity = df_50m.sort_values('vol_mc_ratio', ascending=False)
print(top_liquidity.head(5))
```

### ⚠️ Limitações

- **Rate Limits**: API pública tem limites (30 req/min)
- **Dados em Tempo Real**: Sempre verifique exchanges antes de operar
- **Risco**: Gems são voláteis - faça sua própria análise

---

## 🇺🇸 English

### 📋 What is GEMS SYSTEM?
Automated system to find and analyze low market cap cryptocurrencies (gems) with high return potential.

### 🛠️ Prerequisites
1. Python 3.8+
2. Virtual environment activated (`venv`)
3. CoinMarketCap API Key (optional, increases limits)

### 📦 Installation & Setup

#### 1. Activate Virtual Environment
```bash
cd c:\market_montrezor_system
.venv\Scripts\activate
```

#### 2. Install Dependencies
```bash
pip install requests pandas numpy
```

#### 3. Configure API Key (Optional)
```bash
# Windows
set CMC_API_KEY=your_key_here
```

### 🚀 How to Use

#### Method 1: Direct Execution (Recommended)
```bash
cd gems_system
python gems_finder.py
```

#### Method 2: Batch/PowerShell
```bash
# Windows
run.bat
# or
run.ps1
```

#### Method 3: Jupyter Notebook
```python
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from gems_finder import find_gems_by_ranges

# Search by ranges
coins, df = find_gems_by_ranges()
print(df.head(10))
```

### 📊 Understanding Results

#### Key Columns
- **symbol**: Coin symbol
- **name**: Full name
- **market_cap**: Current Market Cap
- **volume**: 24h Volume
- **vol_mc_ratio**: Volume / Market Cap (liquidity)
- **final_score**: Composite score (0-10)

#### Searched Ranges
- **50m_range**: MC $40M-$60M, Volume >$500K
- **10m_range**: MC $8M-$15M, Volume >$200K

### 💾 Generated Files

#### Structure
```
data/
├── gems_today.csv           # Last execution
├── gems_YYYYMMDD.csv       # Daily snapshot
└── snapshots/
    ├── gems_50m_range_*.csv # 50M range
    ├── gems_10m_range_*.csv # 10M range
    └── gems_consolidated_*.csv # All gems
```

### 🎯 Best Practices

#### 1. Daily Analysis
```python
# Check today's gems
import pandas as pd
df = pd.read_csv('data/gems_today.csv')

# Filter high-score gems
high_score = df[df['final_score'] > 7]
print(high_score.sort_values('final_score', ascending=False))
```

#### 2. Historical Comparison
```python
# Compare today vs yesterday
today = pd.read_csv('data/gems_20260501.csv')
yesterday = pd.read_csv('data/gems_20260430.csv')

# New entries
new_gems = today[~today['symbol'].isin(yesterday['symbol'])]
print(f"New gems: {len(new_gems)}")
```

#### 3. Range Analysis
```python
# Analyze 50M range
df_50m = pd.read_csv('data/snapshots/gems_50m_range_*.csv')
top_liquidity = df_50m.sort_values('vol_mc_ratio', ascending=False)
print(top_liquidity.head(5))
```

### ⚠️ Limitations

- **Rate Limits**: Public API has limits (30 req/min)
- **Real-time Data**: Always check exchanges before trading
- **Risk**: Gems are volatile - do your own research

---

## 🆘 Troubleshooting

### 🇧🇷 Problemas Comuns

#### ModuleNotFoundError
```bash
# Ative o venv primeiro
cd c:\market_montrezor_system
.venv\Scripts\activate
```

#### Rate Limit Exceeded
- **Solução**: Aguarde 1-2 minutos e tente novamente
- **Prevenção**: Use API Key da CoinMarketCap

#### Sem gems encontradas
- **Causa**: Condições de mercado muito voláteis
- **Ação**: Ajuste faixas no código ou aguarde

### 🇺🇸 Common Issues

#### ModuleNotFoundError
```bash
# Activate venv first
cd c:\market_montrezor_system
.venv\Scripts\activate
```

#### Rate Limit Exceeded
- **Solution**: Wait 1-2 minutes and retry
- **Prevention**: Use CoinMarketCap API Key

#### No gems found
- **Cause**: Very volatile market conditions
- **Action**: Adjust ranges in code or wait

---

## 📈 Advanced Usage

### 🇧🇷 Uso Avançado

#### Personalizar Faixas
```python
# Editar gems_finder.py
ranges = {
    'custom_range': {
        'min_mc': 20_000_000,
        'max_mc': 30_000_000,
        'min_volume': 100_000
    }
}
```

#### Adicionar Indicadores
```python
# No arquivo de análise
df['rsi'] = calculate_rsi(df['price'])
df['macd'] = calculate_macd(df['price'])
```

### 🇺🇸 Advanced Usage

#### Customize Ranges
```python
# Edit gems_finder.py
ranges = {
    'custom_range': {
        'min_mc': 20_000_000,
        'max_mc': 30_000_000,
        'min_volume': 100_000
    }
}
```

#### Add Indicators
```python
# In analysis file
df['rsi'] = calculate_rsi(df['price'])
df['macd'] = calculate_macd(df['price'])
```

---

## 📞 Suporte | Support

- **Issues**: Report problems in the project repository
- **Features**: Request new features via GitHub Issues
- **Updates**: Check README.md for latest changes

---

*Última atualização: 2026-05-01* | *Last updated: 2026-05-01*
