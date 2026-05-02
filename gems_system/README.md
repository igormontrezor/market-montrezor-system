# 🚀 GEMS SYSTEM

Sistema especializado para busca e análise de criptomoedas (gems) de baixo market cap com alto potencial.

## 📁 Estrutura

```
gems_system/
├── src/
│   └── gems/
│       ├── __init__.py
│       ├── coin.py          # Classe Coin
│       ├── collector.py     # CoinMarketCap Collector
│       ├── filters.py       # Filtros de gems
│       ├── enricher.py      # Enriquecimento de dados
│       ├── scorer.py        # Cálculo de scores
│       ├── ai.py            # Análise AI
│       └── hunter.py        # Sistema principal
├── data/                    # Snapshots históricos
├── test_cmc.py             # Teste da API CoinMarketCap
├── main.py                 # Execução principal
├── run.bat                 # Execução Windows
└── README.md
```

## 🚀 Uso Rápido

### Via Terminal
```bash
cd gems_system
python main.py
```

### Via Notebook
```python
# No Jupyter Notebook
from src.gems.hunter import GemHunter

hunter = GemHunter()
coins, df = hunter.run()

# 📊 Ver dados
print(df.head(10))

# 🔍 Filtrar gems
df[df["final_score"] > 3]

# 📈 Top gems
df.sort_values("final_score", ascending=False).head(10)

# 💾 Salvar snapshot
hunter.save_snapshot()
```

## 🎯 Funcionalidades

- ✅ Busca automática de gems via CoinMarketCap API
- ✅ Cálculo de score final (quantitativo + AI)
- ✅ Filtragem por market cap e volume
- ✅ Enriquecimento com dados CEX e FDV
- ✅ Snapshots históricos
- ✅ Análise de liquidez
- ✅ Detecção de keywords (AI, RWA, Gaming, etc.)

## 📊 Métricas Calculadas

- **vol_mc_ratio**: Volume / Market Cap
- **final_score**: Score composto para ranking
- **price_change_24h**: Variação de preço 24h

## 💾 Snapshots

O sistema salva snapshots automáticos para análise histórica:

```python
# Salvar com timestamp
hunter.save_snapshot()

# Salvar com nome customizado
hunter.save_snapshot("today")
```

Arquivos salvos em: `data/gems_YYYYMMDD_HHMMSS.csv`

## 🔧 Configuração

### API Key CoinMarketCap
1. Obtenha sua API Key em https://coinmarketcap.com/api/
2. Configure a variável de ambiente:
   ```bash
   # Windows
   set CMC_API_KEY=sua_chave_aqui
   ```

### Testar API
```bash
python test_cmc.py
```

### Extender Análises
- Adicione indicadores técnicos
- Implemente análise de sentimento
- Crie alertas automáticos

## 🚧 Próximos Passos

- [x] Integração com CoinMarketCap API
- [ ] Sistema de alertas
- [ ] Interface web
- [ ] Backtesting de estratégias
- [ ] Machine Learning para previsões

## ⚠️ Importante

Este sistema está separado do sistema principal mas compartilha classes base. Use a mesma venv do projeto principal.
