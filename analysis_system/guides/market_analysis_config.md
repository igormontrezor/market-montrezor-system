# 📊 Sharpe & Sortino Analysis - Estudo Focado

---

## 🎯 Objetivo
Estudo aprofundado de **Sharpe Ratio vs Sortino Ratio** para identificação de topos e fundos em cripto e ativos tradicionais.

---

## ⚙️ Configuração Base

### Dados
- **Fonte:** Yahoo Finance (`yfinance`)
- **Intervalo:** `1wk` (semanal)
- **Período:** 2018-01-01 até atual
- **Ativos:** BTC-USD, SPY, GLD

---

## 🔍 Padrões Sharpe/Sortino Descobertos

### 1) TOPO VERDADEIRO ⚠️
```
Sinal: Sharpe caindo + Sortino esticado
O que significa: Euforia com risco crescendo
Exemplos validados: 2024-03, 2025-07
```

### 2) TOPO FALSO 🚨
```
Sinal: Sharpe caindo + Sortino ainda subindo
O que significa: Divergência = reversão iminente
Exemplo: 2025-10
```

### 3) FUNDO VERDADEIRO ✅
```
Sinal: Sharpe subindo + Sortino começando a subir
O que significa: Recuperação saudável
```

---

## 📈 Interpretação dos Ratios

### Sharpe Ratio (60 semanas)
- **O que mede:** Eficiência geral (retorno / volatilidade total)
- **Sensibilidade:** Alta (detecta mudanças rápidas)
- **Uso:** **ALARME** - primeiro a sinalizar problemas

### Sortino Ratio (90 semanas)
- **O que mede:** Eficiência real (retorno / volatilidade negativa)
- **Sensibilidade:** Média (mais estável)
- **Uso:** **CONFIRMAÇÃO** - saúde estrutural do ativo

## 🎯 Sinais de Trading (Sharpe/Sortino)

### Referent values for SHARPE & SORTINO after REVERSAL(BOTTOM to TOP) BUY!
```
- [ ] (Sharpe > -1.0 & Sortino > -1.0) = Excelent for buy BTC and Large altcoins 📈
- [ ] (Sharpe > 0 & Sortino > -1.0) = Excelent enter for altcoins 🚀
- [ ] (Sharpe > 2.0 & Sortino > 3.0) | (Sortino > 3.0 & Sharpe < 2.0) = End! 🎉
- [ ] Divergence (Sharpe↓, Sortino↑) ← **Strong Sinal**
```
### Referent values for SHARPE & SORTINO after REVERSAL(TOP to BOTTOM) SELL!
```
- [ ] (Sharpe > -2.0 & Sortino > -2.0) | (Sortino > -2.0 & Sharpe > 0) = End! 🎉
```
---

## 🔧 Código Focado (Sharpe & Sortino)

### Janelas Otimizadas
```python
trading_days_sharpe = 60   # semanas (~14 meses) - alarme rápido
trading_days_sortino = 90  # semanas (~17 meses) - saúde estrutural
```

### Annualização (Semanal)
```python
rf = 0.01 / 52                    # taxa livre de risco semanal
```

```python
# Configuração
trading_days_sharpe = 60
trading_days_sortino = 90
rf = 0.01 / 52

# Sharpe Ratio (60 semanas) - ALARME
mean_sharpe = stocks_returns_log_df.rolling(window=trading_days_sharpe).mean()
vol_sharpe = stocks_returns_log_df.rolling(window=trading_days_sharpe).std()
sharpe_ratio = (mean_sharpe - rf) * trading_days_sharpe / vol_sharpe

# Sortino Ratio (90 semanas) - CONFIRMAÇÃO
negative_returns = stocks_returns_log_df[stocks_returns_log_df < 0]
vol_sortino = negative_returns.rolling(window=trading_days_sortino).std() * np.sqrt(trading_days_sortino)
sortino_ratio = (stocks_returns_log_df.rolling(window=trading_days_sortino).mean() - rf) * trading_days_sortino / vol_sortino
```

---

## 📝 Insights Principais (Sharpe/Sortino)

### Descobertas
1. **Sharpe adianta crises** (mais sensível)
2. **Sortino confirma saúde** (mais confiável)
3. **Divergência = sinal poderoso** (Sharpe↓, Sortino↑)
4. **Combinação 60/90 semanas** é ideal para cripto

### Comportamento por Ativo
- **BTC:** Sortino >> Sharpe (assimetria - sobe aos saltos)
- **SPY:** Sortino ≈ Sharpe (simétrico - mais previsível)
- **GLD:** Ambos baixos (conservador - pouco retorno)

---

## 🚀 Próximos Estudos (Futuro)

Para quando dominar Sharpe/Sortino:
- [ ] Adicionar Calmar Ratio
- [ ] Incluir Volume Analysis
- [ ] Testar outros ativos (ETH, SOL)
- [ ] Backtestar estratégia

---

## 📅 Histórico

- **2025-03-28:** Início estudo focado Sharpe/Sortino
- **2025-03-28:** Descoberta padrão 60/90 semanas
- **2025-03-28:** Validação sinais topos/fundos

---

*Foco: Sharpe & Sortino para identificação de topos e fundos*
