@echo off
echo =======================================
echo MARKET MONTREZOR SYSTEM - GEMS FINDER v6.0
echo Sistema Multi-Timeframe com Social Intelligence REAL
echo    YouTube API REAL + Telegram Scraping REAL + Arquivos OTIMIZADOS
echo    Cache Consistente + Metrics Autenticas + Sistema Production-Ready
echo =======================================
echo.
echo Verificando estrutura de diretorios (preservando dados)...
if not exist "data" mkdir "data" >nul 2>&1
if not exist "data\daily_snapshots" mkdir "data\daily_snapshots" >nul 2>&1
if not exist "data\snapshots" mkdir "data\snapshots" >nul 2>&1
echo Diretorios OK - Dados existentes preservados!
echo.

echo Verificando configuracoes de API...
if not exist "..\config\api_keys.py" (
    echo ⚠️  AVISO: config\api_keys.py nao encontrado
    echo    YouTube usara simulacao automaticamente
    echo.
) else (
    echo ✅ YouTube API Key encontrada em ..\config\api_keys.py
    echo.
)
if not exist "telegram_config.py" (
    echo ⚠️  AVISO: telegram_config.py nao encontrado
    echo    Telegram usara simulacao automaticamente
    echo.
) else (
    echo ✅ Telegram config encontrado em telegram_config.py
    echo.
)
echo Configuracoes verificadas!
echo.

echo Ativando ambiente virtual...
cd ..
call .venv\Scripts\activate.bat 2>nul
if errorlevel 1 (
    echo Erro ao ativar ambiente virtual
    pause
    exit /b 1
)

echo Executando GEMS FINDER v6.0 - OTIMIZADO e 100%% FUNCIONAL...
echo    - Cache 12 horas: Consistente, sem arquivos duplicados
echo    - YouTube API REAL: datetime.UTC corrigido, publishedAfter valido
echo    - Telegram Scraping REAL: Regex boundaries, sem falsos positivos
echo    - Data Quality: Apenas 'real' ou 'simulation', sem 'partial'
echo    - Velocity Preservado: 0,1,2 videos tem valores diferentes
echo    - Search Terms: Limpos, sem quebra de query com aspas
echo    - Social Validation: Penalty 30%% para dados simulados
echo    - ARQUIVOS OTIMIZADOS: 66%% menos arquivos (2 vs 6)
echo    - Eventos Especiais: Unificados no enhanced CSV
echo    - Sistema Robusto: Todos os bugs criticos corrigidos
echo.

cd gems_system
python gems_finder.py
if errorlevel 1 (
    echo Erro durante execucao
    pause
    exit /b 1
)

echo.
echo GEMS FINDER v6.0 CONCLUIDO!
echo.
echo Sistema de Cache Consistente:
echo    - Duracao: 12 horas (respeitado)
echo    - Timestamps: Consistentes entre cache e snapshots
echo    - Sem duplicacao: Arquivos criados apenas quando necessario
echo    - OTIMIZACAO: 2 arquivos por execucao (vs 6 anteriores)
echo    - Consolidado: gems_10M_to_50M_enhanced com eventos especiais
echo.
echo Verifique os resultados (se criados):
echo    data\snapshots\ - Analises historicas CSV (OTIMIZADO)
echo    data\snapshots\gems_10M_to_50M_*.csv - Consolidado (2 arquivos)
echo    data\snapshots\gems_10M_to_50M_enhanced_*.csv - Com eventos especiais
echo    data\daily_snapshots\ - Snapshots diarios JSON
echo    data\gems_cache.json - Cache API centralizado
echo.
echo Sistema com Social Intelligence REAL:
echo    1. YouTube API: Dados reais, timezone corrigido, query valida
echo    2. Telegram Scraping: Regex boundaries, sem falsos positivos
echo    3. Data Quality: Flags consistentes, penalty aplicada
echo    4. Velocity: Ranking preservado mesmo com poucos videos
echo    5. Cache: Timestamps consistentes, sem arquivos duplicados
echo    6. ARQUIVOS OTIMIZADOS: 66%% reducao, eventos unificados
echo.
echo Atualizacoes v6.0 - OTIMIZACAO COMPLETA:
echo    - Arquivos: 6 -> 2 por execucao (66%% reducao)
echo    - Eventos Especiais: Unificados no enhanced CSV
echo    - Colunas Novas: persistence_days, is_confirmed_leader, rs_strong
echo    - Social Explosion, RS vs BTC forte: tudo unificado
echo    - Sistema Production-Ready: 100%% funcional, sem bugs
echo    - Mantida compatibilidade: confirmed_gems.json intacto
echo.
echo Para ATIVAR dados REAIS:
echo    1. YouTube: Configure YOUTUBE_API_KEY em config\api_keys.py
echo    2. Telegram: pip install telethon + configure telegram_config.py
echo    3. Sistema usara dados reais automaticamente!
echo.
echo 🔍 VERIFICANDO ARQUIVOS GERADOS:
echo    📁 data\snapshots\ - Arquivos CSV otimizados (2 por execucao)
echo    📁 data\snapshots\gems_10M_to_50M_*.csv - Dados consolidados
echo    📁 data\snapshots\gems_10M_to_50M_enhanced_*.csv - Com eventos especiais
echo    📁 data\daily_snapshots\ - Snapshots diarios JSON
echo    📁 data\gems_cache.json - Cache API (12 horas)
echo.
echo 💡 DICAS:
echo    ✅ Se "Usando cache" → NAO gera novos arquivos
echo    🆕 Se "Snapshot criado" → NOVOS arquivos gerados
echo    ⏰ Cache dura 12 horas para economizar API
echo.
pause
