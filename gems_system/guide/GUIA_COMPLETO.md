# 📊 GEMS SYSTEM - GUIA COMPLETO

## 🎯 **O que é o Sistema?**
Busca criptomoedas (gems) com potencial de valorização usando análise técnica e social.

---

## 🔄 **FLUXO COMPLETO DO SISTEMA**

### **ETAPA 1: Busca de Dados**
```python
# Coleta gems de $10M a $50M da CoinGecko API
# Salva em cache por 12 horas (evita requisições excessivas)
# Cache: data/gems_cache.json
```

### **ETAPA 2: Análise Técnica**
```python
# Filtros aplicados a cada gem:
- Volume/MC Ratio (principal)
- Resiliência de Preço (pullback saudável)
- RS vs BTC (performance relativa)
- Momentum (interesse real)
- Wash Trading detection
```

### **ETAPA 3: Análise Multi-Timeframe (PERSISTÊNCIA)**
```python
# 🔥 ANÁLISE DE PERSISTÊNCIA - CRUCIAL!
# Verifica performance da gem ao longo do tempo

def analyze_timeframe_classification(symbol, historical_data):
    """
    Analisa 3 timeframes:
    - Short term (últimos 3 dias)
    - Medium term (últimos 7 dias) 
    - Long term (últimos 14 dias)
    
    Classifica em:
    - LEADER_CONFIRMED: 7+ dias persistentes
    - LEADER_EMERGING: 5-7 dias persistentes
    - CANDIDATE_STRONG: 3-5 dias persistentes
    - CANDIDATE_INITIAL: 1-3 dias persistentes
    - MONITORING: <1 dia persistente
    """
    
    # Salva em: data/daily_snapshots/daily_YYYYMMDD.json
    # Acumula dados históricos para análise de persistência
```

### **ETAPA 4: Validação Social (YouTube Only)**
```python
# Critério para ativar análise social:
if ratio > 0.5 and persistence_days >= 1:
    # Busca dados do YouTube
    # Calcula velocity (crescimento de views)
    # Classifica: EXPLOSION, STRONG, MODERATE, LOW, WEAK
else:
    # "NÃO APLICÁVEL" - sem análise social
```

### **ETAPA 5: Cálculo de Scores**
```python
# Quant Score (60% do peso):
- Ratio Volume/MC: -0.5 a +1.5 pontos
- Resiliência: +0.5 pontos
- RS vs BTC: +0.1 a +0.4 pontos
- Momentum: +0.1 a +0.3 pontos
- Potencial Ouro: +0.5 pontos
- Penalidade Wash Trading: -0.3 pontos

# Social Score (40% do peso):
- SOCIAL_EXPLOSION: +3.0 pontos
- SOCIAL_STRONG: +2.0 pontos
- SOCIAL_MODERATE: +1.0 ponto
- SOCIAL_LOW: 0.0 ponto
- SOCIAL_WEAK: -1.0 ponto

# Final Score:
final_score = (quant_score * 0.6) + (social_score * 0.4)
```

---

## 📁 **GERAÇÃO DE ARQUIVOS CSV**

### **Quando são gerados?**
```python
# A cada execução com dados novos:
- Se cache expirou OU
- Se encontrou gems diferentes

# Arquivos criados:
1. gems_10M_to_50M_YYYYMMDD_HHMMSS.csv
   - Dados brutos das gems
   
2. gems_10M_to_50M_enhanced_YYYYMMDD_HHMMSS.csv  
   - Dados + scores + eventos especiais
```

### **Persistência de Dados**
```python
# Daily snapshots (acumulado):
data/daily_snapshots/daily_YYYYMMDD.json
- Salva todas as gems encontradas no dia
- Usado para calcular persistência (timeframe analysis)
- Mantém histórico para identificar líderes confirmados

# Cache temporário:
data/gems_cache.json
- Válido por 12 horas
- Evita requisições excessivas à API
- Atualizado automaticamente quando expira
```

---

## 🏆 **EVENTOS ESPECIAIS**

### **1. Líderes Confirmados**
```python
# Critério:
timeframe_classification == "LEADER_CONFIRMED"

# Requer:
- 7+ dias de persistência forte
- Performance consistente across timeframes
- Dados históricos suficientes

# Primeira execução = sempre 0 (precisa acumular dados)
```

### **2. RS vs BTC Forte**
```python
# Critério:
btc_change_24h < 0 AND rs_24h >= 2.0

# Lógica:
- BTC caindo (mercado ruim)
- Gem subindo mais que BTC (força relativa)
- Sinal de liderança em bear market

# Exemplo:
- BTC: -5%
- Gem: +3%
- RS = 8% (forte!)
```

### **3. Explosão Social**
```python
# Critério:
combined_validation == "SOCIAL_EXPLOSION"

# Requer:
- YouTube velocity >= 1.4
- Ratio > 0.5 E persistência >= 1 dia
- Dados sociais reais (não simulados)

# YouTube velocity:
- Calcula crescimento de views recentes
- Compara com média histórica
- Identifica spikes de interesse
```

---

## 📊 **SISTEMA DE PONTUAÇÃO DETALHADO**

### **Quant Score (Técnico)**
```python
def _calculate_quant_score(gem):
    score = 0.0
    
    # 1. Volume/MC Ratio (fator principal)
    ratio = gem.get('ratio', 0)
    if ratio >= 1.0:      score += 1.5  # Breakout
    elif ratio >= 0.7:    score += 1.0  # Strong
    elif ratio >= 0.5:    score += 0.5  # Moderate
    elif ratio >= 0.2:    score += 0.0  # Low
    else:                 score -= 0.5  # Muito baixo
    
    # 2. Resiliência de Preço
    if gem.get('price_resilience'): score += 0.5
    
    # 3. Potencial Ouro
    if gem.get('is_gold'): score += 0.5
    
    # 4. RS vs BTC
    rs_24h = gem.get('rs_24h')
    btc_24h = gem.get('btc_change_24h')
    if btc_24h < 0 and rs_24h >= 4.0: score += 0.4
    elif btc_24h < 0 and rs_24h >= 2.0: score += 0.2
    elif rs_24h >= 2.0: score += 0.1
    
    # 5. Momentum
    momentum = gem.get('momentum')
    if momentum == 'high': score += 0.3
    elif momentum == 'medium': score += 0.1
    
    # 6. Penalidades
    if gem.get('suspected_wash_trading'): score -= 0.3
    if gem.get('volume_recovery'): score += 0.2
    
    return max(-1.0, min(3.0, score))
```

### **Social Score (YouTube)**
```python
def get_youtube_only_validation(youtube_velocity):
    """
    Baseado apenas no YouTube velocity:
    - velocity >= 1.4: SOCIAL_EXPLOSION (+3.0)
    - velocity >= 1.1: SOCIAL_STRONG (+2.0)
    - velocity >= 0.85: SOCIAL_MODERATE (+1.0)
    - velocity >= 0.8: SOCIAL_LOW (0.0)
    - velocity < 0.8: SOCIAL_WEAK (-1.0)
    """
```

---

## 🔄 **CICLO DE VIDA DO SISTEMA**

### **Execução Diária**
```python
1. 🌅 Início do dia
   - Cache vazio (primeira execução)
   - Busca dados frescos da API
   
2. 📊 Análise técnica
   - Aplica todos os filtros
   - Calcula scores quantitativos
   
3. 🧠 Análise social
   - Apenas gems com ratio > 0.5
   - Apenas com persistência >= 1 dia
   
4. 💾 Salvamento
   - Cria CSVs do dia
   - Atualiza daily snapshot
   
5. 🏆 Identificação de líderes
   - Compara com dados históricos
   - Classifica por persistência
```

### **Acumulação de Dados**
```python
# Dia 1: 0 líderes (sem histórico)
# Dia 2: 0 líderes (precisa 3+ dias)
# Dia 3: CANDIDATE_INITIAL
# Dia 5: CANDIDATE_STRONG  
# Dia 7: LEADER_EMERGING
# Dia 10: LEADER_CONFIRMADO
```

---

## 🎯 **EXEMPLO PRÁTICO**

### **Gem: AIXBT**
```python
# Dados técnicos:
- Market Cap: $34.8M
- Volume: $22.7M  
- Ratio: 0.65 (Strong)
- RS 24h: +5.49%
- BTC 24h: +0.03%
- Persistência: 1 dia (primeira execução)

# Análise:
Quant Score: +1.0 (ratio) + 0.1 (RS) = 1.1
Social Score: 0.0 (não aplicável)
Final Score: (1.1 × 0.6) + (0.0 × 0.4) = 0.66

# Eventos:
- Líder confirmado: ❌ (precisa 7+ dias)
- RS vs BTC forte: ❌ (BTC positivo)
- Explosão social: ❌ (não aplicável)
```

---

## 📈 **MÉTRICAS DE SUCESSO**

### **O que procurar:**
```python
✅ Gems com ratio > 0.7 (volume real)
✅ RS vs BTC forte em bear markets
✅ Líderes confirmados (7+ dias persistentes)
✅ Explosões sociais (YouTube spikes)
✅ Potencial ouro (pullback + volume)
```

### **O que evitar:**
```python
❌ Ratio < 0.2 (volume morto)
❌ Wash trading suspeito
❌ Sem persistência (one-day wonders)
❌ Social simulado (APIs falsas)
```

---

## 🚀 **PRÓXIMOS PASSOS**

### **Curto Prazo (1-7 dias)**
- Acumular dados históricos
- Identificar candidates iniciais
- Calcular persistência real

### **Médio Prazo (1-4 semanas)**
- Encontrar líderes emergentes
- Detectar RS vs BTC forte
- Validar explosões sociais

### **Longo Prazo (1+ meses)**
- Líderes confirmados estáveis
- Sistema de backtesting
- Otimização de parâmetros

---

## 📝 **RESUMO EXECUTIVO**

**O sistema é um filtro multi-camadas:**

1. **Filtro 1:** Volume/MC ratio (elimina 99% das cryptos)
2. **Filtro 2:** Análise técnica (RS, momentum, resiliência)
3. **Filtro 3:** Persistência (timeframe analysis)
4. **Filtro 4:** Validação social (YouTube)
5. **Score:** 60% técnico + 40% social
6. **Output:** CSV com gems + scores + eventos

**Foco: Gems com volume real, técnica forte e potencial de liderança.** 🎯
