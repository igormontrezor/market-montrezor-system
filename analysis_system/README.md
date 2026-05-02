# ANALYSIS SYSTEM

Sistema de análise de mercado para criptomoedas.

## 📁 Estrutura

```
analysis_system/
├── README.md                    (este arquivo)
├── run_analysis.py              (execução principal)
├── run.bat                      (execução Windows)
├── run.ps1                      (execução PowerShell)
├── market_analysis_config.md    (configurações)
├── market_analysis_diagrams.drawio (diagramas)
├── tarefas_pendentes.md         (tarefas)
├── main.py                      (módulo principal)
├── assets/                      (recursos)
├── data/                        (dados)
├── examples/                    (exemplos)
├── indicators/                  (indicadores técnicos)
├── notebooks/                   (notebooks de análise)
│   ├── market_analysis_month.ipynb
│   ├── market_analysis_oop.ipynb
│   └── market_analysis_week.ipynb
├── plotting/                    (gráficos)
├── signals/                     (sinais)
└── strategies/                  (estratégias)
```

## 🚀 Execução

### Windows (Batch)
```bash
run.bat
```

### Windows (PowerShell)
```powershell
.\run.ps1
```

### Direto
```bash
python run_analysis.py
```

## 🔧 Configuração

- Usa o config compartilhado: `../config/`
- Usa o venv compartilhado: `../.venv/`

## 📊 Funcionalidades

- Análise técnica
- Indicadores
- Sinais de trading
- Estratégias
- Gráficos e visualizações

## 📝 Notas

Este sistema compartilha:
- Configurações com `gems_system`
- Ambiente virtual (`.venv`)
- Bibliotecas do projeto principal
