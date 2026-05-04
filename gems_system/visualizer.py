#!/usr/bin/env python3
"""
📊 Visualizador interativo com Plotly + Pandas - Versão Corrigida
Correção principal: bloco global (evolução histórica) agora aparece
em QUALQUER fluxo — snapshot único ou comparação múltipla.
"""
import os
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime
import webbrowser
import tempfile
from evolution_functions import (
    get_all_snapshots_for_evolution,
    analyze_historical_evolution,
    determine_evolution_status,
    create_evolution_timeline,
    create_hall_of_fame,
    get_evolution_color,
    get_evolution_emoji
)


# ===========================================================================
# ✅ NOVO: Função central que monta o bloco global de evolução histórica.
# Antes ficava enterrada dentro de create_top10_comparison_chart() e só
# era atingida pelo fluxo de comparação múltipla. Agora é independente e
# pode ser chamada de qualquer lugar.
# ===========================================================================

def build_global_evolution_block(reference_dfs, snapshot_info):
    """
    Monta o bloco completo de análise histórica global.

    Parâmetros
    ----------
    reference_dfs   : lista de DataFrames dos snapshots selecionados pelo usuário
                      (usado apenas como âncora para score_change recente).
    snapshot_info   : lista de dicts com metadados dos snapshots selecionados.

    Retorna
    -------
    js_block  : string com o JavaScript Plotly para os gráficos globais.
    summary   : string HTML com tabela de resumo / tendências.
    hall      : string HTML com Hall da Fama.
    """

    # 1. Carregar TODOS os snapshots do disco
    all_snapshots_data = get_all_snapshots_for_evolution()
    global_dfs = [s['df'] for s in all_snapshots_data if isinstance(s, dict) and 'df' in s]

    if not global_dfs:
        empty = "<p style='color:#666;'>⚠️ Nenhum snapshot histórico encontrado em data/snapshots.</p>"
        return "", empty, empty

    # 2. Análise histórica completa
    historical_data = analyze_historical_evolution(all_snapshots_data, reference_dfs)

    # 3. Montar ranking global (baseado em TODOS os snapshots do disco)
    global_crypto_data = {}
    for i, df in enumerate(global_dfs):
        if 'final_score' in df.columns:
            sorted_df = df.sort_values('final_score', ascending=False)
            score_col = 'final_score'
        elif 'ratio' in df.columns:
            sorted_df = df.sort_values('ratio', ascending=False)
            score_col = 'ratio'
        else:
            sorted_df = df.sort_values('market_cap', ascending=False)
            score_col = 'market_cap'

        for _, row in sorted_df.head(20).iterrows():
            symbol = row.get('symbol')
            if not symbol:
                continue

            score   = float(row[score_col])          if pd.notna(row.get(score_col))                    else 0
            mc      = float(row['market_cap'])        if pd.notna(row.get('market_cap'))                 else 0
            volume  = float(row['total_volume'])      if pd.notna(row.get('total_volume'))               else 0
            change  = float(row['price_change_percentage_24h']) if pd.notna(row.get('price_change_percentage_24h')) else 0
            sector  = row.get('sector', 'Unknown')
            category= row.get('category', row.get('timeframe_classification', 'Unknown'))

            if symbol not in global_crypto_data:
                global_crypto_data[symbol] = {
                    'scores': [], 'mcs': [], 'volumes': [], 'changes_24h': [],
                    'periods_present': [], 'total_periods': len(global_dfs),
                    'sector': sector, 'category': category
                }

            global_crypto_data[symbol]['scores'].append(score)
            global_crypto_data[symbol]['mcs'].append(mc)
            global_crypto_data[symbol]['volumes'].append(volume)
            global_crypto_data[symbol]['changes_24h'].append(change)
            global_crypto_data[symbol]['periods_present'].append(i)

    global_crypto_ranking = []
    for symbol, data in global_crypto_data.items():
        avg_score       = sum(data['scores']) / len(data['scores'])
        consistency     = len(data['periods_present']) / data['total_periods']
        avg_mc          = sum(data['mcs'])          / len(data['mcs'])
        avg_volume      = sum(data['volumes'])      / len(data['volumes'])
        avg_change      = sum(data['changes_24h'])  / len(data['changes_24h'])
        evolution_status= determine_evolution_status(symbol, historical_data, data['periods_present'])

        first_period = 0 in data['periods_present']
        last_period  = (len(global_dfs) - 1) in data['periods_present']

        if consistency == 1.0:
            presence_type = 'consistent'
        elif first_period and not last_period:
            presence_type = 'gone'
        elif not first_period and last_period:
            presence_type = 'new'
        else:
            presence_type = 'intermittent'

        if len(data['scores']) > 1:
            mean_s   = avg_score
            variance = sum((x - mean_s) ** 2 for x in data['scores']) / len(data['scores'])
            score_volatility = variance ** 0.5
        else:
            score_volatility = 0

        global_crypto_ranking.append({
            'symbol': symbol,
            'avg_score': avg_score,
            'consistency': consistency,
            'avg_mc': avg_mc,
            'avg_volume': avg_volume,
            'avg_change': avg_change,
            'score_volatility': score_volatility,
            'presence_type': presence_type,
            'evolution_status': evolution_status,
            'periods_present': data['periods_present'],
            'scores': data['scores'],
            'mcs': data['mcs'],
            'volumes': data['volumes'],
            'changes_24h': data['changes_24h'],
            'sector': data['sector'],
            'category': data['category']
        })

    global_crypto_ranking.sort(
        key=lambda x: (x['avg_score'], x['consistency'], x['avg_mc']),
        reverse=True
    )

    top15_global = global_crypto_ranking[:15]

    # 4. Injetar referências nos historical_data para hall_of_fame e tendências
    historical_data['crypto_ranking'] = global_crypto_ranking
    historical_data['global_dfs']     = global_dfs

    # 5. Calcular score_change para o último snapshot selecionado pelo usuário
    last_reference_df = reference_dfs[-1] if reference_dfs else None
    if last_reference_df is not None and len(global_dfs) >= 2:
        first_scores = dict(zip(global_dfs[0]['symbol'],  global_dfs[0].get('final_score', global_dfs[0].get('ratio', pd.Series()))))
        last_scores  = dict(zip(global_dfs[-1]['symbol'], global_dfs[-1].get('final_score', global_dfs[-1].get('ratio', pd.Series()))))
        score_changes = []
        for _, row in last_reference_df.iterrows():
            sym = row['symbol']
            score_changes.append(last_scores.get(sym, 0) - first_scores.get(sym, 0))
        last_reference_df = last_reference_df.copy()
        last_reference_df['score_change'] = score_changes

    # 6. Gerar JS dos gráficos e HTML das seções
    # Usa global_dfs como base para os gráficos (histórico completo)
    js_block = create_all_comparison_charts(
        top15_global, snapshot_info, global_crypto_ranking, global_dfs, historical_data
    )

    summary  = create_advanced_summary_table(
        top15_global, global_crypto_ranking,
        len(global_dfs), historical_data, last_reference_df
    )

    hall     = create_hall_of_fame(historical_data, snapshot_info)

    return js_block, summary, hall


# ===========================================================================
# HTML base para o bloco global (divs + script).
# Usado tanto no dashboard de snapshot único quanto no de comparação.
# ===========================================================================

def _global_block_html(js_block, summary_html, hall_html):
    """Retorna o HTML completo do bloco global de evolução com tutoriais."""
    return f"""
    <div style="background-color: #ecf0f1; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
        <h3>📈 ANÁLISE HISTÓRICA GLOBAL (todos os snapshots)</h3>

        <!-- Gráfico 1: Bubble Chart (MAIS IMPORTANTE) -->
        <div id="bubble-chart" style="margin-top: 30px;"></div>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #e74c3c;">
            <h4 style="margin-top: 0; color: #2c3e50;">🫧 <strong>Tutorial - Bubble Chart (O Mais Importante!)</strong></h4>
            <p style="margin-bottom: 10px;"><strong>O que mostra:</strong> Relação entre Market Cap, Ratio e Volume em 3D.</p>
            <p style="margin-bottom: 10px;"><strong>Eixos:</strong></p>
            <ul style="margin-left: 20px; margin-bottom: 10px;">
                <li><strong>X (horizontal):</strong> Market Cap - tamanho da moeda</li>
                <li><strong>Y (vertical):</strong> Ratio Volume/MC - interesse real</li>
                <li><strong>Tamanho da bolha:</strong> Volume total negociado</li>
            </ul>
            <p style="margin-bottom: 10px;"><strong>Quadrantes valiosos:</strong></p>
            <ul style="margin-left: 20px; margin-bottom: 10px;">
                <li><strong>🔥 Superior Esquerdo:</strong> MC baixo + Ratio alto = OURO PURO!</li>
                <li><strong>🚀 Inferior Direito:</strong> MC alto + Ratio baixo = dinheiro dormindo</li>
            </ul>
            <p style="margin-bottom: 0;"><strong>Exemplo prático:</strong>Bolhas que sobem gradualmente no eixo do ratio, aumentam de tamanho de forma consistente e mantêm posição ao longo do tempo indicam entrada sustentável de capital — candidatas reais a liderança.</p>
        </div>

        <!-- Gráfico 2: Acumulação Silenciosa (2º MAIS IMPORTANTE) -->
        <div id="accumulation-chart" style="margin-top: 30px;"></div>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #27ae60;">
            <h4 style="margin-top: 0; color: #2c3e50;">🤫 <strong>Tutorial - Gráfico de Acumulação Silenciosa</strong></h4>
            <p style="margin-bottom: 10px;"><strong>O que mostra:</strong> Gems com aumento gradual do ratio (dinheiro inteligente acumulando).</p>
            <p style="margin-bottom: 10px;"><strong>Como interpretar:</strong></p>
            <ul style="margin-left: 20px; margin-bottom: 10px;">
                <li><strong>Linhas subindo suavemente:</strong> Acumulação saudável (smart money)</li>
                <li><strong>Picos abruptos:</strong> Spikes especulativos</li>
                <li><strong>Platôs altos:</strong> Acumulação consolidada</li>
            </ul>
            <p style="margin-bottom: 0;"><strong>Exemplo prático:</strong> Uma gem com ratio subindo 0.2→0.4→0.6→0.8 em semanas está sendo acumulada por grandes players - prepare-se!</p>
        </div>

        <!-- Gráfico 3: Heatmap Setorial -->
        <div id="sector-heatmap" style="margin-top: 30px;"></div>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #16a085;">
            <h4 style="margin-top: 0; color: #2c3e50;">🏭 <strong>Tutorial - Heatmap Setorial</strong></h4>
            <p style="margin-bottom: 10px;"><strong>O que mostra:</strong> Quais setores estão "quentes" ou "frios" pela cor.</p>
            <p style="margin-bottom: 10px;"><strong>Escala de cores (branco → vermelho escuro):</strong></p>
            <ul style="margin-left: 20px; margin-bottom: 10px;">
                <li><strong>⚪ Branco/Amarelo claro:</strong> Setores FRIOS (ratio baixo, sem interesse)</li>
                <li><strong>🟡 Amarelo/Laranja:</strong> Setores AQUECENDO (dinheiro entrando)</li>
                <li><strong>🔴 Laranja/Vermelho escuro:</strong> Setores QUENTES (muito dinheiro, potencial de topo)</li>
            </ul>
            <p style="margin-bottom: 10px;"><strong>Estratégia por cor:</strong></p>
            <ul style="margin-left: 20px; margin-bottom: 10px;">
                <li><strong>Comprar nos brancos/amarelos:</strong> Entrar antes do dinheiro</li>
                <li><strong>Vender nos vermelhos escuros:</strong> Realizar lucro no pico</li>
                <li><strong>Observar laranjas:</strong> Setor em movimento forte</li>
            </ul>
            <p style="margin-bottom: 0;"><strong>Exemplo prático:</strong>Setores frios devem ser observados para sinais iniciais de entrada de capital. Setores em aquecimento representam as melhores oportunidades de entrada. Setores quentes indicam forte fluxo, mas exigem análise de continuidade ou exaustão antes de decisões.</p>
        </div>

        <!-- Gráfico 4: Heatmap de Persistência -->
        <div id="persistence-heatmap" style="margin-top: 30px;"></div>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #f39c12;">
            <h4 style="margin-top: 0; color: #2c3e50;">🔥 <strong>Tutorial - Heatmap de Persistência</strong></h4>
            <p style="margin-bottom: 10px;"><strong>O que mostra:</strong> Quais gems foram consistentes em cada snapshot.</p>
            <p style="margin-bottom: 10px;"><strong>Como interpretar:</strong></p>
            <ul style="margin-left: 20px; margin-bottom: 10px;">
                <li><strong>⚪ Branco:</strong> Gem ausente no snapshot</li>
                <li><strong>🟢 Verde claro:</strong> Gem aparecendo (ratio baixo, começando)</li>
                <li><strong>🟢 Verde escuro:</strong> Gem forte e consistente (ratio alto)</li>
                <li><strong>🟣 Gaps brancos:</strong> Gem que aparece e some (spike, não confiável)</li>
            </ul>
            <p style="margin-bottom: 0;"><strong>Exemplo prático:</strong> Uma linha verde horizontal contínua indica uma gem que nunca decepcionou - excelente para longo prazo!</p>
        </div>

        <!-- Gráfico 5: Evolução Temporal -->
        <div id="top10-comparison-chart" style="margin-top: 30px;"></div>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #3498db;">
            <h4 style="margin-top: 0; color: #2c3e50;">📊 <strong>Tutorial - Gráfico de Evolução Temporal</strong></h4>
            <p style="margin-bottom: 10px;"><strong>O que mostra:</strong> A evolução do Ratio Volume/MC das top 10 gems ao longo do tempo.</p>
            <p style="margin-bottom: 10px;"><strong>Como interpretar:</strong></p>
            <ul style="margin-left: 20px; margin-bottom: 10px;">
                <li><strong>Linhas subindo:</strong> Gems ganhando interesse e volume real</li>
                <li><strong>Linhas estáveis altas:</strong> Gems consolidadas com liquidez constante</li>
                <li><strong>Linhas caindo:</strong> Gems perdendo interesse/volume</li>
            </ul>
            <p style="margin-bottom: 0;"><strong>Exemplo prático:</strong> Se uma gem apresenta um pico de ratio (ex: 0.3 → 1.2), retorna e estabiliza em nível igual ou superior ao anterior, sem tendência de queda contínua, isso pode indicar retenção de interesse e possível acumulação — especialmente se combinado com força relativa contra o BTC.</p>
        </div>

        <!-- Gráfico 6: Consistência -->
        <div id="evolution-chart" style="margin-top: 30px;"></div>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #9b59b6;">
            <h4 style="margin-top: 0; color: #2c3e50;">📈 <strong>Tutorial - Gráfico de Consistência</strong></h4>
            <p style="margin-bottom: 10px;"><strong>O que mostra:</strong> Quantos dias cada gem manteve-se forte (ratio > 0.5).</p>
            <p style="margin-bottom: 10px;"><strong>Como interpretar:</strong></p>
            <ul style="margin-left: 20px; margin-bottom: 10px;">
                <li><strong>Barras altas:</strong> Gems persistentes (líderes de altseason)</li>
                <li><strong>Barras médias:</strong> Gems emergentes com potencial</li>
                <li><strong>Barras baixas:</strong> Gems com picos rápidos (spikes)</li>
            </ul>
            <p style="margin-bottom: 0;"><strong>Exemplo prático:</strong> Uma gem com 15+ dias de consistência é provavelmente uma líder real. Uma com 2-3 dias pode ser apenas um spike.</p>
        </div>

        <div id="ranking-summary"     style="margin-top: 20px;"></div>
        <div id="hall-of-fame"        style="margin-top: 20px;"></div>
    </div>

    <script>
        {js_block}
        document.getElementById('ranking-summary').innerHTML = `{summary_html.replace('`', chr(96))}`;
        document.getElementById('hall-of-fame').innerHTML    = `{hall_html.replace('`', chr(96))}`;
    </script>
    """


# ===========================================================================
# create_interactive_dashboard — CORRIGIDO
# Agora inclui o bloco global de evolução histórica.
# ===========================================================================

def create_interactive_dashboard(df, file_name):
    """Cria dashboard interativo com Plotly — inclui bloco global histórico."""

    if 'ratio' not in df.columns:
        df['ratio'] = df['total_volume'].fillna(0) / df['market_cap']

    # --- Gráficos do snapshot selecionado (comportamento original) ---
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '🏆 Top 15 Market Cap',       '📈 Top 15 Volume/MC Ratio',
            '🚀 Top 15 Variação 24h',     '🎯 Top 15 Final Score'
        ),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )

    top_mc = df.nlargest(15, 'market_cap')
    fig.add_trace(go.Bar(x=top_mc['symbol'], y=top_mc['market_cap'],
                         name='Market Cap', marker_color='#3498db'), row=1, col=1)

    top_ratio = df.nlargest(15, 'ratio')
    fig.add_trace(go.Bar(x=top_ratio['symbol'], y=top_ratio['ratio'],
                         name='Volume/MC Ratio', marker_color='#e74c3c'), row=1, col=2)

    top_change = df.nlargest(15, 'price_change_percentage_24h')
    bar_colors = ['#2ecc71' if x > 0 else '#e74c3c'
                  for x in top_change['price_change_percentage_24h']]
    fig.add_trace(go.Bar(x=top_change['symbol'], y=top_change['price_change_percentage_24h'],
                         name='Variação 24h', marker_color=bar_colors), row=2, col=1)

    score_col = 'final_score' if 'final_score' in df.columns else 'ratio'
    top_score = df.nlargest(15, score_col)
    fig.add_trace(go.Bar(x=top_score['symbol'], y=top_score[score_col],
                         name='Final Score', marker_color='#f39c12'), row=2, col=2)

    fig.update_layout(
        title=f'🚀 GEMS SYSTEM DASHBOARD - {file_name}',
        height=800, showlegend=False, template='plotly_white'
    )

    fig_table = create_interactive_table(df)

    # --- ✅ Bloco global histórico ---
    snapshot_info = [{'file': file_name, 'date': datetime.now().strftime('%Y-%m-%d %H:%M'), 'index': 0, 'count': len(df)}]
    js_block, summary_html, hall_html = build_global_evolution_block([df], snapshot_info)
    global_html = _global_block_html(js_block, summary_html, hall_html)

    # --- HTML final ---
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 GEMS SYSTEM DASHBOARD</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; text-align: center; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            .stats {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 GEMS SYSTEM DASHBOARD</h1>
            <p><strong>Arquivo:</strong> {file_name}</p>
            <p><strong>Data:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Gems:</strong> {len(df)} | <strong>Colunas:</strong> {len(df.columns)}</p>

            <div class="stats">
                <h3>📊 Estatísticas do Snapshot</h3>
                <p><strong>Market Cap Médio:</strong> ${df['market_cap'].mean():,.0f}</p>
                <p><strong>Volume Total:</strong> ${df['total_volume'].sum():,.0f}</p>
                <p><strong>Variação 24h Positivas:</strong>
                    {(df['price_change_percentage_24h'] > 0).sum()}/{len(df)}
                    ({(df['price_change_percentage_24h'] > 0).mean()*100:.1f}%)
                </p>
            </div>

            <!-- Gráficos do snapshot -->
            <div id="dashboard"></div>
            <div id="table" style="margin-top: 30px;"></div>

            <!-- ✅ Bloco global histórico (aparece sempre) -->
            {global_html}
        </div>

        <script>
            {fig.to_html(div_id="dashboard", include_plotlyjs=False)}
            {fig_table.to_html(div_id="table", include_plotlyjs=False)}
        </script>
    </body>
    </html>
    """

    _open_in_browser(html_content)
    return df


# ===========================================================================
# create_advanced_dashboard — CORRIGIDO
# Agora usa build_global_evolution_block em vez de duplicar a lógica.
# ===========================================================================

def create_advanced_dashboard(dfs, snapshot_info):
    """Cria dashboard avançado com abas + bloco global histórico."""

    # ✅ Bloco global: usa build_global_evolution_block (lê TODOS os snapshots do disco)
    js_block, summary_html, hall_html = build_global_evolution_block(dfs, snapshot_info)
    global_html = _global_block_html(js_block, summary_html, hall_html)

    # Abas por período
    tabs_buttons = ""
    tabs_contents = ""
    for i, (df, info) in enumerate(zip(dfs, snapshot_info)):
        active = "active" if i == 0 else ""
        tabs_buttons  += f'<button class="tab {active}" onclick="showTab({i})">Período {i+1} - {info["date"]}</button>\n'
        tabs_contents += f'<div id="tab-{i}" class="tab-content {active}">{create_period_html(df, info, i)}</div>\n'

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>📊 GEMS SYSTEM - COMPARATIVO AVANÇADO</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; text-align: center; }}
            .tabs {{ display: flex; border-bottom: 2px solid #3498db; margin-bottom: 20px; flex-wrap: wrap; }}
            .tab {{ padding: 12px 20px; cursor: pointer; border: none; background: #ecf0f1; margin-right: 5px; border-radius: 5px 5px 0 0; }}
            .tab.active {{ background: #3498db; color: white; }}
            .tab-content {{ display: none; }}
            .tab-content.active {{ display: block; }}
            .filters {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            .filter-item {{ margin: 10px 0; }}
            .stats {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .period-summary {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .period-item {{ margin: 10px 0; padding: 10px; border-left: 4px solid #3498db; background-color: white; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 GEMS SYSTEM - COMPARATIVO AVANÇADO</h1>

            <!-- ✅ Bloco global histórico (sempre presente) -->
            {global_html}

            <!-- Períodos selecionados -->
            <div class="period-summary">
                <h3>📅 Períodos Comparados (seleção atual)</h3>
                {''.join([f'<div class="period-item"><strong>Período {info["index"]+1}:</strong> {info["date"]} ({info["count"]} gems)</div>' for info in snapshot_info])}
            </div>

            <!-- Filtros -->
            <div class="filters">
                <h3>🔍 Filtros Interativos</h3>
                <div class="filter-item">
                    <label>Filtrar por Symbol:</label>
                    <input type="text" id="symbolFilter" placeholder="Ex: BTC" onkeyup="filterData()">
                </div>
                <div class="filter-item">
                    <label>Score mínimo:</label>
                    <input type="number" id="scoreFilter" step="0.1" min="0" max="1" value="0" onkeyup="filterData()">
                </div>
                <div class="filter-item">
                    <label>Market Cap mínimo:</label>
                    <input type="number" id="mcFilter" step="1000000" min="0" value="0" onkeyup="filterData()">
                </div>
                <div class="filter-item">
                    <label>Mostrar apenas:</label>
                    <select id="showFilter" onchange="filterData()">
                        <option value="all">Todas as cryptos</option>
                        <option value="consistent">Presente em todos períodos</option>
                        <option value="new">Novas no último período</option>
                        <option value="gone">Saíram do último período</option>
                    </select>
                </div>
            </div>

            <!-- Abas dos períodos selecionados -->
            <div class="tabs">
                {tabs_buttons}
            </div>
            {tabs_contents}
        </div>

        <script>
            function showTab(tabIndex) {{
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                const target = document.getElementById('tab-' + tabIndex);
                if (target) target.classList.add('active');
                const tabs = document.querySelectorAll('.tab');
                if (tabs[tabIndex]) tabs[tabIndex].classList.add('active');
            }}

            function filterData() {{
                const symbolFilter = document.getElementById('symbolFilter').value.toUpperCase();
                const scoreFilter  = parseFloat(document.getElementById('scoreFilter').value) || 0;
                const mcFilter     = parseFloat(document.getElementById('mcFilter').value) || 0;

                for (let i = 0; i < {len(dfs)}; i++) {{
                    const table = document.querySelector('#tab-' + i + ' table');
                    if (!table) continue;
                    const rows = table.getElementsByTagName('tr');
                    for (let row of rows) {{
                        if (row.rowIndex === 0) continue;
                        const cells  = row.getElementsByTagName('td');
                        const symbol = cells[0] ? cells[0].textContent.toUpperCase() : '';
                        const score  = cells[5] ? parseFloat(cells[5].textContent) || 0 : 0;
                        const mc     = cells[2] ? parseFloat(cells[2].textContent.replace(/[$,]/g, '')) || 0 : 0;
                        let show = true;
                        if (symbolFilter && !symbol.includes(symbolFilter)) show = false;
                        if (score < scoreFilter) show = false;
                        if (mc < mcFilter) show = false;
                        row.style.display = show ? '' : 'none';
                    }}
                }}
            }}
        </script>
    </body>
    </html>
    """

    _open_in_browser(html_content)


# ===========================================================================
# Utilitário: abrir no navegador e limpar arquivo temporário
# ===========================================================================

def _open_in_browser(html_content):
    import threading, time
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_content)
        temp_file = f.name

    print("🌐 Abrindo visualização no navegador...")
    webbrowser.open(f'file://{temp_file}')

    def cleanup():
        time.sleep(5)
        try:
            os.unlink(temp_file)
        except:
            pass

    t = threading.Thread(target=cleanup, daemon=True)
    t.start()


# ===========================================================================
# Funções auxiliares — sem alterações de lógica, apenas mantidas aqui
# para o arquivo ser autossuficiente.
# ===========================================================================

def _fig_to_plotly_newplot_js(fig, div_id):
    fig_json   = fig.to_plotly_json()
    data_json  = json.dumps(fig_json.get('data',   []), ensure_ascii=False)
    layout_json= json.dumps(fig_json.get('layout', {}), ensure_ascii=False)
    return f"Plotly.newPlot('{div_id}', {data_json}, {layout_json}, {{responsive: true}});"


def create_all_comparison_charts(top10, snapshot_info, crypto_ranking, dfs, historical_data=None):
    """Gráficos comparativos: evolução temporal e consistência."""

    def get_top5_consistent_cryptos():
        crypto_appearances = {}
        for df_cur in dfs:
            if df_cur is None or df_cur.empty or 'final_score' not in df_cur.columns:
                continue
            df_sorted = df_cur.sort_values('final_score', ascending=False).reset_index(drop=True)
            for _, row in df_sorted.head(5).iterrows():
                sym = row.get('symbol')
                if sym:
                    crypto_appearances[sym] = crypto_appearances.get(sym, 0) + 1
        return sorted(crypto_appearances.items(), key=lambda x: x[1], reverse=True)[:5]

    top5_cryptos = get_top5_consistent_cryptos()

    # Gráfico 1: Evolução temporal
    fig1 = go.Figure()
    for symbol, appearances in top5_cryptos:
        scores_timeline  = []
        periods_timeline = []
        for i, df in enumerate(dfs):
            df_sorted = df.sort_values('final_score', ascending=False).reset_index(drop=True)
            df_sorted['_rank'] = df_sorted.index + 1
            row = df_sorted[df_sorted['symbol'] == symbol]
            if not row.empty and int(row.iloc[0]['_rank']) <= 5:
                scores_timeline.append(float(row.iloc[0]['final_score']))
            else:
                scores_timeline.append(None)
            periods_timeline.append(f'P{i+1}')

        fig1.add_trace(go.Scatter(
            x=periods_timeline, y=scores_timeline,
            mode='lines+markers',
            name=f'{symbol} ({appearances}x)',
            line=dict(width=3), marker=dict(size=8),
            connectgaps=False
        ))

    fig1.update_layout(
        title='📈 EVOLUÇÃO TEMPORAL — TOP 5 MAIS CONSISTENTES (Histórico Completo)',
        xaxis_title='Períodos', yaxis_title='Score',
        height=500, template='plotly_white', hovermode='x unified'
    )

    # Gráfico 2: Consistência
    consistent_data = sorted(
        [item for item in crypto_ranking if item['consistency'] == 1.0],
        key=lambda x: x['avg_score'], reverse=True
    )
    bar_colors = ['#27ae60' if item['avg_score'] > 0.8 else '#95a5a6' for item in consistent_data]

    fig2 = go.Figure(data=[go.Bar(
        x=[item['symbol']    for item in consistent_data],
        y=[item['avg_score'] for item in consistent_data],
        marker_color=bar_colors,
        text=[f'{item["avg_score"]:.3f}' for item in consistent_data],
        textposition='auto',
        hovertext=[f'{item["symbol"]}<br>Score: {item["avg_score"]:.3f}' for item in consistent_data],
        hoverinfo='text'
    )])

    fig2.update_layout(
        title='💎 CRYPTOS 100% CONSISTENTES (Presentes em todos os períodos)',
        xaxis_title='Cryptomoedas', yaxis_title='Score Médio',
        height=400, template='plotly_white'
    )

    # Gráfico 3: Bubble Chart — Ratio vs MC vs Score
    fig3 = create_bubble_chart(crypto_ranking)

    # Gráfico 4: Heatmap de Persistência
    fig4 = create_persistence_heatmap(crypto_ranking, dfs)

    # Gráfico 5: Acumulação Silenciosa
    fig5 = create_accumulation_chart(crypto_ranking, dfs)

    # Gráfico 6: Heatmap Setorial
    fig6 = create_sector_heatmap(crypto_ranking, dfs)

    return "\n".join([
        "// Gráfico 1: Evolução Temporal",
        _fig_to_plotly_newplot_js(fig1, "top10-comparison-chart"),
        "// Gráfico 2: Consistência",
        _fig_to_plotly_newplot_js(fig2, "evolution-chart"),
        "// Gráfico 3: Bubble Chart",
        _fig_to_plotly_newplot_js(fig3, "bubble-chart"),
        "// Gráfico 4: Heatmap de Persistência",
        _fig_to_plotly_newplot_js(fig4, "persistence-heatmap"),
        "// Gráfico 5: Acumulação Silenciosa",
        _fig_to_plotly_newplot_js(fig5, "accumulation-chart"),
        "// Gráfico 6: Heatmap Setorial",
        _fig_to_plotly_newplot_js(fig6, "sector-heatmap"),
    ])


def create_bubble_chart(crypto_ranking):
    """
    🫧 Bubble Chart — Ratio vs Market Cap vs Final Score

    Eixo X  = Market Cap (escala log para não achatar os menores)
    Eixo Y  = Ratio Volume/MC  (o filtro central do sistema)
    Tamanho = Final Score médio (quanto maior a bolha, melhor o score)
    Cor     = Zona predominante (early_accumulation / strong / breakout / mixed)

    Leitura rápida:
      - Bolhas grandes no canto superior esquerdo = MC pequeno, ratio alto, score alto
        → candidatas ideais (alta oportunidade, liquidez real)
      - Bolhas pequenas no canto inferior direito = MC grande, ratio baixo
        → ignorar ou monitorar
    """

    zone_color_map = {
        'breakout':          '#e74c3c',   # vermelho — máxima prioridade
        'strong':            '#f39c12',   # laranja  — forte
        'early_accumulation':'#3498db',   # azul     — acumulação
        'mixed':             '#9b59b6',   # roxo     — misto
        'unknown':           '#95a5a6',   # cinza
    }

    symbols, x_mc, y_ratio, sizes, colors, hover = [], [], [], [], [], []

    for item in crypto_ranking:
        avg_mc    = item.get('avg_mc',    0)
        avg_score = item.get('avg_score', 0)
        # Ratio médio: recalcula a partir dos volumes e mcs armazenados
        vols = item.get('volumes', [])
        mcs  = item.get('mcs',    [])
        if mcs and any(m > 0 for m in mcs):
            avg_ratio = sum(v / m for v, m in zip(vols, mcs) if m > 0) / sum(1 for m in mcs if m > 0)
        else:
            avg_ratio = 0

        if avg_mc <= 0 or avg_ratio <= 0:
            continue

        # Determinar zona predominante
        scores_list = item.get('scores', [])
        if avg_ratio >= 1.0:
            zone = 'breakout'
        elif avg_ratio >= 0.5:
            zone = 'strong'
        elif avg_ratio >= 0.2:
            zone = 'early_accumulation'
        else:
            zone = 'unknown'

        # Tamanho proporcional ao score (mínimo visível = 8, máximo = 50)
        bubble_size = max(8, min(50, avg_score * 40))

        symbols.append(item['symbol'])
        x_mc.append(avg_mc)
        y_ratio.append(avg_ratio)
        sizes.append(bubble_size)
        colors.append(zone_color_map.get(zone, '#95a5a6'))
        hover.append(
            f"<b>{item['symbol']}</b><br>"
            f"MC médio: ${avg_mc:,.0f}<br>"
            f"Ratio médio: {avg_ratio:.2f}<br>"
            f"Score médio: {avg_score:.3f}<br>"
            f"Consistência: {item['consistency']*100:.0f}%<br>"
            f"Zona: {zone}<br>"
            f"Presença: {len(item['periods_present'])} snapshots"
        )

    fig = go.Figure()

    # Adicionar por zona para ter legenda separada
    for zone_label, zone_color in zone_color_map.items():
        if zone_label == 'mixed':
            continue
        idx = [i for i, c in enumerate(colors) if c == zone_color]
        if not idx:
            continue
        fig.add_trace(go.Scatter(
            x=[x_mc[i]   for i in idx],
            y=[y_ratio[i] for i in idx],
            mode='markers+text',
            name=zone_label.replace('_', ' ').title(),
            text=[symbols[i] for i in idx],
            textposition='top center',
            textfont=dict(size=9),
            marker=dict(
                size=[sizes[i] for i in idx],
                color=zone_color,
                opacity=0.75,
                line=dict(width=1, color='white')
            ),
            hovertext=[hover[i] for i in idx],
            hoverinfo='text'
        ))

    # Linha de referência ratio = 1.0 (breakout threshold)
    if x_mc:
        x_range = [min(x_mc) * 0.8, max(x_mc) * 1.2]
        fig.add_shape(type='line', x0=x_range[0], x1=x_range[1], y0=1.0, y1=1.0,
                      line=dict(color='#e74c3c', width=1, dash='dash'))
        fig.add_annotation(x=x_range[1], y=1.0, text='Breakout ≥1.0',
                           showarrow=False, font=dict(color='#e74c3c', size=10),
                           xanchor='right')

        # Linha de referência ratio = 0.5 (strong threshold)
        fig.add_shape(type='line', x0=x_range[0], x1=x_range[1], y0=0.5, y1=0.5,
                      line=dict(color='#f39c12', width=1, dash='dot'))
        fig.add_annotation(x=x_range[1], y=0.5, text='Strong ≥0.5',
                           showarrow=False, font=dict(color='#f39c12', size=10),
                           xanchor='right')

    fig.update_layout(
        title='🫧 BUBBLE CHART — Ratio vs Market Cap (tamanho = Score)',
        xaxis=dict(
            title='Market Cap (USD)',
            type='log',
            tickformat='$,.0f',
        ),
        yaxis=dict(title='Ratio Volume/MC', rangemode='tozero'),
        height=600,
        template='plotly_white',
        hovermode='closest',
        legend=dict(title='Zona', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )

    return fig


def create_persistence_heatmap(crypto_ranking, dfs):
    """
    📊 Heatmap de Persistência — Ratio por snapshot ao longo do tempo

    Linhas  = cryptos (ordenadas por score médio descendente, top 25)
    Colunas = snapshots em ordem cronológica (P1 → Pn)
    Cor     = ratio Volume/MC naquele snapshot (0 = ausente / branco)

    Leitura rápida:
      - Linha toda verde escuro → ratio alto e consistente → candidata forte
      - Linha com gaps brancos  → aparece e some → spike, não tendência
      - Linha verde ficando mais escura da esquerda p/ direita → acelerando
    """

    # Pegar top 25 por score médio para não poluir o gráfico
    top_items = sorted(crypto_ranking, key=lambda x: x['avg_score'], reverse=True)[:25]

    n_periods = len(dfs)
    period_labels = [f'P{i+1}' for i in range(n_periods)]
    symbol_labels = [item['symbol'] for item in top_items]

    # Montar matriz: linhas = cryptos, colunas = períodos
    matrix = []
    annotations = []

    for row_idx, item in enumerate(top_items):
        row_ratios = []
        vols_per_period = item.get('volumes', [])
        mcs_per_period  = item.get('mcs',     [])
        periods_present = item.get('periods_present', [])

        for col_idx in range(n_periods):
            if col_idx in periods_present:
                # Encontrar o índice dentro dos dados do item
                data_idx = periods_present.index(col_idx)
                v = vols_per_period[data_idx] if data_idx < len(vols_per_period) else 0
                m = mcs_per_period[data_idx]  if data_idx < len(mcs_per_period)  else 0
                ratio = v / m if m > 0 else 0
            else:
                ratio = 0  # Ausente

            row_ratios.append(ratio)

            # Anotação do valor dentro da célula (só se presente)
            if ratio > 0:
                annotations.append(dict(
                    x=col_idx, y=row_idx,
                    text=f'{ratio:.1f}',
                    font=dict(size=8, color='white' if ratio > 0.7 else 'black'),
                    showarrow=False
                ))

        matrix.append(row_ratios)

    # Colorscale: branco (ausente/baixo) → verde forte (ratio alto)
    colorscale = [
        [0.0,  'rgba(255,255,255,0)'],   # 0   = ausente (transparente/branco)
        [0.01, '#f0f9e8'],               # trace
        [0.2,  '#bae4b3'],               # early accumulation
        [0.5,  '#74c476'],               # strong
        [0.8,  '#31a354'],               # forte
        [1.0,  '#006d2c'],               # breakout
    ]

    # Normalizar: ratio máximo observado como teto da escala
    all_ratios = [r for row in matrix for r in row if r > 0]
    zmax = max(all_ratios) if all_ratios else 2.0
    zmax = min(zmax, 3.0)  # Limitar para não distorcer por outliers

    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=period_labels,
        y=symbol_labels,
        colorscale=colorscale,
        zmin=0,
        zmax=zmax,
        colorbar=dict(
            title='Ratio V/MC',
            tickvals=[0, 0.5, 1.0, 1.5, 2.0],
            ticktext=['Ausente', '0.5', '1.0 🔥', '1.5', '2.0+']
        ),
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>Período: %{x}<br>Ratio: %{z:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title='📊 HEATMAP DE PERSISTÊNCIA — Ratio Volume/MC por Snapshot (Top 25)',
        xaxis=dict(title='Snapshots (cronológico →)', side='top'),
        yaxis=dict(title='Cryptos (ordenado por Score ↓)', autorange='reversed'),
        height=max(400, 25 * len(top_items) + 100),
        template='plotly_white',
        annotations=annotations,
    )

    return fig


def create_accumulation_chart(crypto_ranking, dfs):
    """
    📈 Gráfico de Acumulação Silenciosa

    Mostra o slope do ratio ao longo do tempo para as top gems.
    Barras horizontais ordenadas por accumulation_score.
    Verde = acumulando / Cinza = sem sinal / Vermelho = caindo.

    Só plota gems que têm accumulation_score > 0 nos dados.
    Caso os dados não tenham a coluna (execuções antigas), usa
    o slope calculado a partir da série de ratios disponível.
    """

    items_with_score = []

    for item in crypto_ranking:
        symbol = item['symbol']

        # Tentar pegar accumulation_score dos dados enriquecidos
        acc_score  = 0.0
        acc_signal = 'none'
        acc_slope  = 0.0

        # Procurar nos DataFrames carregados
        for df in dfs:
            if df is None or df.empty:
                continue
            row = df[df['symbol'] == symbol]
            if not row.empty:
                acc_score  = float(row.iloc[0].get('accumulation_score',  0) or 0)
                acc_signal = str(row.iloc[0].get('accumulation_signal', 'none') or 'none')
                acc_slope  = float(row.iloc[0].get('accumulation_slope',  0) or 0)
                break

        # Fallback: calcular slope da série de ratios do ranking global
        if acc_score == 0.0:
            vols = item.get('volumes', [])
            mcs  = item.get('mcs',    [])
            if len(vols) >= 3 and any(m > 0 for m in mcs):
                ratios = [v / m for v, m in zip(vols, mcs) if m > 0]
                n      = len(ratios)
                xs     = list(range(n))
                mean_x = sum(xs) / n
                mean_y = sum(ratios) / n
                num    = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ratios))
                den    = sum((x - mean_x) ** 2 for x in xs)
                slope  = num / den if den != 0 else 0.0
                acc_slope = slope
                if slope > 0.01:
                    acc_score  = min(slope / 0.05, 1.0) * 0.6
                    acc_signal = 'moderate' if acc_score >= 0.4 else 'weak'

        if acc_score > 0.05 or abs(acc_slope) > 0.005:
            items_with_score.append({
                'symbol':  symbol,
                'score':   acc_score,
                'signal':  acc_signal,
                'slope':   acc_slope,
                'avg_score': item.get('avg_score', 0)
            })

    if not items_with_score:
        # Retorna gráfico vazio com mensagem
        fig = go.Figure()
        fig.add_annotation(
            text='Dados de acumulação ainda não disponíveis.<br>'
                 'Execute o gems_finder com o módulo accumulation_sector integrado.',
            xref='paper', yref='paper', x=0.5, y=0.5,
            showarrow=False, font=dict(size=14, color='#666')
        )
        fig.update_layout(title='📈 ACUMULAÇÃO SILENCIOSA', height=300, template='plotly_white')
        return fig

    # Ordenar por score descendente, top 20
    items_with_score.sort(key=lambda x: x['score'], reverse=True)
    items_with_score = items_with_score[:20]

    symbols = [i['symbol'] for i in items_with_score]
    scores  = [i['score']  for i in items_with_score]
    slopes  = [i['slope']  for i in items_with_score]
    signals = [i['signal'] for i in items_with_score]

    signal_color_map = {
        'very_strong': '#006d2c',
        'strong':      '#31a354',
        'moderate':    '#74c476',
        'weak':        '#bae4b3',
        'none':        '#95a5a6',
    }
    bar_colors = [signal_color_map.get(s, '#95a5a6') for s in signals]

    hover = [
        f'<b>{i["symbol"]}</b><br>'
        f'Acc Score: {i["score"]:.3f}<br>'
        f'Slope ratio: {i["slope"]:+.4f}<br>'
        f'Sinal: {i["signal"]}<br>'
        f'Score médio geral: {i["avg_score"]:.3f}'
        for i in items_with_score
    ]

    fig = go.Figure(data=[go.Bar(
        x=scores,
        y=symbols,
        orientation='h',
        marker_color=bar_colors,
        text=[f'{s:+.4f}' for s in slopes],
        textposition='outside',
        hovertext=hover,
        hoverinfo='text'
    )])

    # Linha de referência — threshold de confirmação
    fig.add_vline(x=0.6, line_dash='dash', line_color='#31a354',
                  annotation_text='Confirmado ≥0.6', annotation_position='top')
    fig.add_vline(x=0.4, line_dash='dot',  line_color='#74c476',
                  annotation_text='Monitorar ≥0.4', annotation_position='top')

    fig.update_layout(
        title='📈 ACUMULAÇÃO SILENCIOSA — Score por Crypto (slope do ratio ao longo do tempo)',
        xaxis=dict(title='Accumulation Score (0–1)', range=[0, 1.05]),
        yaxis=dict(title='', autorange='reversed'),
        height=max(350, 30 * len(items_with_score) + 80),
        template='plotly_white',
        showlegend=False
    )

    return fig


def create_sector_heatmap(crypto_ranking, dfs):
    """
    🏭 Heatmap Setorial — Temperatura por setor ao longo dos snapshots

    Linhas  = setores (L1, L2, DeFi, Gaming, AI, Meme, Infra, RWA…)
    Colunas = snapshots em ordem cronológica
    Cor     = ratio médio do setor naquele snapshot

    Leitura:
      - Linha toda quente → setor consistentemente ativo
      - Múltiplas linhas aquecendo ao mesmo tempo → sinal de rotação ampla
    """
    try:
        from accumulation_sector import get_sector, SectorCorrelationAnalyzer
    except ImportError:
        fig = go.Figure()
        fig.add_annotation(
            text='Módulo accumulation_sector.py não encontrado.<br>'
                 'Copie-o para a pasta do projeto.',
            xref='paper', yref='paper', x=0.5, y=0.5,
            showarrow=False, font=dict(size=13, color='#e74c3c')
        )
        fig.update_layout(title='🏭 ANÁLISE SETORIAL', height=300, template='plotly_white')
        return fig

    analyzer = SectorCorrelationAnalyzer()

    # Montar snapshots setoriais a partir dos global dfs
    n_periods     = len(dfs)
    period_labels = [f'P{i+1}' for i in range(n_periods)]
    all_sectors   = set()
    snap_analyses = []

    for df in dfs:
        if df is None or df.empty:
            snap_analyses.append({})
            continue
        gems = df.to_dict(orient='records')
        # Enriquecer com setor se não tiver
        for gem in gems:
            if 'sector' not in gem or not gem['sector']:
                gem['sector'] = get_sector(gem.get('symbol', '').lower())
        analysis = analyzer.analyze_snapshot(gems)
        snap_analyses.append(analysis.get('sectors', {}))
        all_sectors.update(analysis.get('sectors', {}).keys())

    if not all_sectors:
        fig = go.Figure()
        fig.add_annotation(
            text='Dados setoriais insuficientes.<br>Necessário pelo menos 1 snapshot com dados enriquecidos.',
            xref='paper', yref='paper', x=0.5, y=0.5,
            showarrow=False, font=dict(size=13, color='#666')
        )
        fig.update_layout(title='🏭 ANÁLISE SETORIAL', height=300, template='plotly_white')
        return fig

    # Ordenar setores por ratio médio geral (mais quente no topo)
    sector_avg = {}
    for sector in all_sectors:
        vals = [s[sector]['avg_ratio'] for s in snap_analyses if sector in s]
        sector_avg[sector] = sum(vals) / len(vals) if vals else 0

    sorted_sectors = sorted(all_sectors, key=lambda s: sector_avg[s], reverse=True)

    # Montar matriz
    matrix       = []
    annotations  = []
    sector_labels= []

    for row_idx, sector in enumerate(sorted_sectors):
        row = []
        for col_idx, snap in enumerate(snap_analyses):
            if sector in snap:
                val = snap[sector]['avg_ratio']
                hot = snap[sector].get('hot_gems', 0)
                temp= snap[sector].get('temperature', 'COLD')
            else:
                val  = 0
                hot  = 0
                temp = 'COLD'
            row.append(val)

            if val > 0:
                annotations.append(dict(
                    x=col_idx, y=row_idx,
                    text=f'{val:.2f}',
                    font=dict(size=8, color='white' if val > 0.5 else 'black'),
                    showarrow=False
                ))

        matrix.append(row)
        sector_labels.append(sector)

    colorscale = [
        [0.0,  '#f5f5f5'],
        [0.15, '#fee8c8'],   # COLD
        [0.35, '#fdbb84'],   # WARMING
        [0.6,  '#e34a33'],   # HOT
        [1.0,  '#7f0000'],   # BLAZING
    ]

    all_vals = [v for row in matrix for v in row if v > 0]
    zmax     = min(max(all_vals) if all_vals else 1.5, 2.0)

    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=period_labels,
        y=sector_labels,
        colorscale=colorscale,
        zmin=0,
        zmax=zmax,
        colorbar=dict(
            title='Ratio médio',
            tickvals=[0, 0.3, 0.5, 0.8, 1.2],
            ticktext=['Frio', '0.3', '0.5🔥', '0.8', '1.2🚨']
        ),
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>Período: %{x}<br>Ratio médio: %{z:.3f}<extra></extra>'
    ))

    fig.update_layout(
        title='🏭 HEATMAP SETORIAL — Ratio médio por setor × snapshot (rotação de capital)',
        xaxis=dict(title='Snapshots (cronológico →)', side='top'),
        yaxis=dict(title='Setor (mais quente ↑)'),
        height=max(350, 40 * len(sorted_sectors) + 120),
        template='plotly_white',
        annotations=annotations
    )

    return fig


def create_advanced_summary_table(top10, crypto_ranking, total_periods, historical_data=None, last_df=None):
    """Tabela de resumo com tendências globais e recentes."""

    global_dfs = historical_data.get('global_dfs', []) if historical_data else []

    # Calcular deltas
    delta_global_dict = {}
    delta_recent_dict = {}

    if len(global_dfs) >= 2:
        df_first = global_dfs[0]
        df_last  = global_dfs[-1]

        score_col_first = 'final_score' if 'final_score' in df_first.columns else 'ratio'
        score_col_last  = 'final_score' if 'final_score' in df_last.columns  else 'ratio'

        first_scores = dict(zip(df_first['symbol'], df_first[score_col_first]))
        last_scores  = dict(zip(df_last['symbol'],  df_last[score_col_last]))

        for sym in set(first_scores) | set(last_scores):
            delta_global_dict[sym] = last_scores.get(sym, 0) - first_scores.get(sym, 0)

        # Recente: adaptativo — nunca igual ao global
        # Usa janela de 5, mas mínimo índice 1 para não repetir o global
        RECENT_WINDOW = 5
        recent_index  = max(len(global_dfs) - RECENT_WINDOW, 1)
        df_recent_ref = global_dfs[recent_index]
        score_col_rec = 'final_score' if 'final_score' in df_recent_ref.columns else 'ratio'
        recent_ref_scores = dict(zip(df_recent_ref['symbol'], df_recent_ref[score_col_rec]))
        for sym in set(recent_ref_scores) | set(last_scores):
            delta_recent_dict[sym] = last_scores.get(sym, 0) - recent_ref_scores.get(sym, 0)

    for item in crypto_ranking:
        item['delta_global'] = delta_global_dict.get(item['symbol'], 0)
        item['delta_recent'] = delta_recent_dict.get(item['symbol'], 0)

    top_growers_global = sorted([c for c in crypto_ranking if c['delta_global'] > 0],
                                 key=lambda x: x['delta_global'], reverse=True)[:5]
    top_fallers_global = sorted([c for c in crypto_ranking if c['delta_global'] < 0],
                                 key=lambda x: x['delta_global'])[:5]
    top_growers_recent = sorted([c for c in crypto_ranking if c['delta_recent'] > 0],
                                 key=lambda x: x['delta_recent'], reverse=True)[:5]
    top_fallers_recent = sorted([c for c in crypto_ranking if c['delta_recent'] < 0],
                                 key=lambda x: x['delta_recent'])[:5]

    def render_trend_block(title, growers, fallers, delta_key):
        growers_html = ''.join([f'<tr><td>{i["symbol"]}</td><td>+{i[delta_key]:.3f}</td></tr>' for i in growers])
        fallers_html = ''.join([f'<tr><td>{i["symbol"]}</td><td>{i[delta_key]:.3f}</td></tr>'  for i in fallers])
        no_data = '<tr><td colspan="2" style="text-align:center;color:#666;">Nenhum dado</td></tr>'
        return f"""
        <div style="background:#f8f9fa;padding:15px;border-radius:5px;margin:20px 0;">
            <h4>{title}</h4>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:15px;">
                <div>
                    <h5>🚀 Maiores Crescimentos</h5>
                    <table style="width:100%;border-collapse:collapse;">
                        <tr style="background:#27ae60;color:white;"><th style="padding:6px;">Crypto</th><th style="padding:6px;">Δ Score</th></tr>
                        {growers_html or no_data}
                    </table>
                </div>
                <div>
                    <h5>⚠️ Maiores Quedas</h5>
                    <table style="width:100%;border-collapse:collapse;">
                        <tr style="background:#e74c3c;color:white;"><th style="padding:6px;">Crypto</th><th style="padding:6px;">Δ Score</th></tr>
                        {fallers_html or no_data}
                    </table>
                </div>
            </div>
        </div>"""

    trends_html = render_trend_block(
        f'📈 TENDÊNCIAS GLOBAIS (desde o 1º snapshot — {len(global_dfs)} snapshots no histórico)',
        top_growers_global, top_fallers_global, 'delta_global'
    )

    # Recentes: só mostra se recent_index > 0 (ou seja, recente != global)
    if len(global_dfs) >= 3:
        RECENT_WINDOW = 5
        recent_index  = max(len(global_dfs) - RECENT_WINDOW, 1)
        snapshots_back = len(global_dfs) - recent_index
        trends_html += render_trend_block(
            f'⚡ TENDÊNCIAS RECENTES (últimos {snapshots_back} snapshots)',
            top_growers_recent, top_fallers_recent, 'delta_recent'
        )
    else:
        trends_html += """
        <div style="background:#f8f9fa;padding:15px;border-radius:5px;margin:20px 0;">
            <h4>⚡ TENDÊNCIAS RECENTES</h4>
            <p style="text-align:center;color:#666;padding:20px;">
                Necessário pelo menos 3 snapshots para calcular tendências recentes.<br>
                Histórico atual: {len(global_dfs)} snapshot(s).
            </p>
        </div>"""

    total_unique    = len(crypto_ranking)
    consistent_count= len([i for i in crypto_ranking if i['consistency'] == 1.0])
    new_count       = len([i for i in crypto_ranking if i['presence_type'] == 'new'])
    gone_count      = len([i for i in crypto_ranking if i['presence_type'] == 'gone'])
    avg_score_geral = sum(i['avg_score'] for i in crypto_ranking) / total_unique if total_unique else 0
    rotatividade    = (new_count + gone_count) / total_unique * 100 if total_unique else 0

    top5_performers = sorted(crypto_ranking, key=lambda x: x['avg_score'], reverse=True)[:5]

    return f"""
    <div class="stats">
        <div style="background:#f8f9fa;padding:15px;border-radius:5px;margin:20px 0;">
            <h4>RESUMO GERAL — Histórico completo ({len(global_dfs)} snapshots)</h4>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-bottom:15px;">
                <div style="text-align:center;background:white;padding:10px;border-radius:5px;">
                    <strong>{total_unique}</strong><br><small>Total Cryptos</small>
                </div>
                <div style="text-align:center;background:white;padding:10px;border-radius:5px;">
                    <strong>{rotatividade:.1f}%</strong><br><small>Rotatividade</small>
                </div>
                <div style="text-align:center;background:white;padding:10px;border-radius:5px;">
                    <strong>{avg_score_geral:.3f}</strong><br><small>Score Médio Geral</small>
                </div>
            </div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:15px;">
                <div style="text-align:center;background:white;padding:10px;border-radius:5px;">
                    <strong>{consistent_count}</strong><br><small>100% Consistentes</small>
                </div>
                <div style="text-align:center;background:white;padding:10px;border-radius:5px;">
                    <strong>{new_count}</strong><br><small>Novas</small>
                </div>
                <div style="text-align:center;background:white;padding:10px;border-radius:5px;">
                    <strong>{gone_count}</strong><br><small>Saíram</small>
                </div>
            </div>
        </div>

        <div style="background:#f8f9fa;padding:15px;border-radius:5px;margin:20px 0;">
            <h4>TOP PERFORMERS (Score médio histórico)</h4>
            <table style="width:100%;border-collapse:collapse;">
                <tr style="background:#27ae60;color:white;">
                    <th style="padding:8px;text-align:left;">Crypto</th>
                    <th style="padding:8px;text-align:center;">Score Médio</th>
                    <th style="padding:8px;text-align:center;">Consistência</th>
                    <th style="padding:8px;text-align:center;">Performance</th>
                </tr>
                {''.join([f"""
                <tr>
                    <td style="padding:8px;"><strong>{i['symbol']}</strong></td>
                    <td style="padding:8px;text-align:center;">{i['avg_score']:.3f}</td>
                    <td style="padding:8px;text-align:center;">{i['consistency']*100:.0f}%</td>
                    <td style="padding:8px;text-align:center;">{"🔥" if i['avg_score'] > 0.8 else "⭐" if i['avg_score'] > 0.6 else "📊"}</td>
                </tr>""" for i in top5_performers])}
            </table>
        </div>

        {trends_html}
    </div>
    """


def create_interactive_table(df):
    """Tabela interativa Plotly com todas as colunas disponíveis."""

    display_cols = ['symbol', 'name', 'market_cap', 'total_volume', 'price_change_percentage_24h']
    for col in ['ratio', 'final_score',
                'persistence_count_3d', 'persistence_count_7d', 'persistence_count_14d',
                'timeframe_classification', 'is_confirmed_leader',
                'zone', 'momentum', 'is_gold', 'rs_strong']:
        if col in df.columns:
            display_cols.append(col)

    table_df = df[[c for c in display_cols if c in df.columns]].copy()

    table_df['market_cap']               = table_df['market_cap'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else 'N/A')
    table_df['total_volume']             = table_df['total_volume'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else 'N/A')
    table_df['price_change_percentage_24h'] = table_df['price_change_percentage_24h'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else 'N/A')

    if 'ratio'       in table_df.columns: table_df['ratio']       = table_df['ratio'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')
    if 'final_score' in table_df.columns: table_df['final_score'] = table_df['final_score'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')

    if 'persistence_count_3d' in table_df.columns:
        for c in ['persistence_count_3d','persistence_count_7d','persistence_count_14d']:
            if c in table_df.columns:
                table_df[c] = table_df[c].apply(lambda x: f"{x}x")

    if 'is_confirmed_leader' in table_df.columns:
        table_df['is_confirmed_leader'] = table_df['is_confirmed_leader'].apply(lambda x: '👑 YES' if x else '❌ NO')

    column_mapping = {
        'symbol':'Symbol','name':'Name','market_cap':'Market Cap','total_volume':'Volume',
        'price_change_percentage_24h':'24h%','ratio':'Ratio','final_score':'Score',
        'persistence_count_3d':'3d','persistence_count_7d':'7d','persistence_count_14d':'14d',
        'timeframe_classification':'Classification','is_confirmed_leader':'Leader',
        'zone':'Zone','momentum':'Momentum','is_gold':'Gold','rs_strong':'RS'
    }
    table_df.rename(columns=column_mapping, inplace=True)

    fig_table = go.Figure(data=[go.Table(
        header=dict(values=list(table_df.columns), fill_color='#3498db', align='left', font=dict(color='white', size=12)),
        cells=dict(values=[table_df[col] for col in table_df.columns], fill_color='lavender', align='left', font=dict(color='black', size=11))
    )])
    fig_table.update_layout(title="📊 DADOS COMPLETOS", title_x=0.5, height=600, template='plotly_white')
    return fig_table


def create_period_html(df, snapshot_info, index):
    """HTML de um período específico (aba na comparação)."""

    display_cols = ['symbol', 'name', 'market_cap', 'total_volume', 'price_change_percentage_24h']
    for col in ['ratio', 'final_score',
                'persistence_count_3d', 'persistence_count_7d', 'persistence_count_14d',
                'timeframe_classification', 'is_confirmed_leader',
                'zone', 'momentum', 'is_gold', 'rs_strong']:
        if col in df.columns:
            display_cols.append(col)

    table_df = df[[c for c in display_cols if c in df.columns]].copy()

    sort_col = 'final_score' if 'final_score' in table_df.columns else 'ratio' if 'ratio' in table_df.columns else None
    if sort_col:
        table_df = table_df.sort_values(sort_col, ascending=False)

    table_df['market_cap']               = table_df['market_cap'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else 'N/A')
    table_df['total_volume']             = table_df['total_volume'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else 'N/A')
    table_df['price_change_percentage_24h'] = table_df['price_change_percentage_24h'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else 'N/A')
    if 'ratio'       in table_df.columns: table_df['ratio']       = table_df['ratio'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')
    if 'final_score' in table_df.columns: table_df['final_score'] = table_df['final_score'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')
    if 'is_confirmed_leader' in table_df.columns:
        table_df['is_confirmed_leader'] = table_df['is_confirmed_leader'].apply(lambda x: '👑 YES' if x else '❌ NO')

    column_mapping = {
        'symbol':'Symbol','name':'Name','market_cap':'Market Cap','total_volume':'Volume',
        'price_change_percentage_24h':'24h%','ratio':'Ratio','final_score':'Score',
        'persistence_count_3d':'3d','persistence_count_7d':'7d','persistence_count_14d':'14d',
        'timeframe_classification':'Classification','is_confirmed_leader':'Leader',
        'zone':'Zone','momentum':'Momentum','is_gold':'Gold','rs_strong':'RS'
    }
    table_df.rename(columns=column_mapping, inplace=True)

    mc_mean  = df['market_cap'].mean()
    vol_sum  = df['total_volume'].sum()
    pos_pct  = (df['price_change_percentage_24h'] > 0).mean() * 100
    pos_cnt  = (df['price_change_percentage_24h'] > 0).sum()

    return f"""
    <div class="stats">
        <h3>📊 Estatísticas — {snapshot_info['date']}</h3>
        <p><strong>Market Cap Médio:</strong> ${mc_mean:,.0f}</p>
        <p><strong>Volume Total:</strong> ${vol_sum:,.0f}</p>
        <p><strong>Variação 24h Positivas:</strong> {pos_cnt}/{len(df)} ({pos_pct:.1f}%)</p>
    </div>
    <h3>📋 Dados Completos — {snapshot_info['date']}</h3>
    {table_df.to_html(classes='table table-striped', index=False)}
    """


# ===========================================================================
# Funções de menu — sem alterações
# ===========================================================================

def get_available_snapshots():
    snapshots_dir = "data/snapshots"
    if not os.path.exists(snapshots_dir):
        return []
    csv_files = [f for f in os.listdir(snapshots_dir) if f.endswith('.csv') and 'enhanced_' in f]
    csv_files.sort(reverse=True)
    return csv_files


def show_snapshot_selection():
    csv_files = get_available_snapshots()
    if not csv_files:
        print("❌ Nenhum snapshot encontrado")
        return None

    print("📁 Snapshots disponíveis:")
    print("0. 📊 Mais recente (automático)")
    for i, file in enumerate(csv_files[:10], 1):
        try:
            date_part = file.split('enhanced_')[1].replace('.csv', '')
            date_str  = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]} {date_part[9:11]}:{date_part[11:13]}"
            print(f"{i:2d}. {file} ({date_str})")
        except:
            print(f"{i:2d}. {file}")
    print()

    while True:
        try:
            choice = input(f"Escolha snapshot (0-{min(len(csv_files), 10)}): ").strip()
            if choice == '0':
                return csv_files[0]
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < min(len(csv_files), 10):
                    return csv_files[idx]
                else:
                    print("❌ Número fora do range")
            else:
                print("❌ Digite um número válido")
        except KeyboardInterrupt:
            return None
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None


def show_comparison_snapshots():
    csv_files = get_available_snapshots()
    if len(csv_files) < 2:
        print("❌ Precisa de pelo menos 2 snapshots para comparar")
        return

    print("📊 COMPARAÇÃO DE SNAPSHOTS:")
    print("1. ⭐ Avançado — últimos 2 snapshots")
    print("2. ⭐ Avançado — escolher quantidade (2-10)")
    print("3. ⭐ Avançado — escolher snapshots específicos")
    print("0. ⬅️  Voltar")
    print()

    choice = input("Opção (0-3): ").strip()

    if choice in ('', '1'):
        _load_and_compare(csv_files[:2])
    elif choice == '2':
        qty_str = input("Quantidade de snapshots (2-10): ").strip()
        try:
            qty = max(2, min(10, int(qty_str)))
            _load_and_compare(csv_files[:qty])
        except:
            print("❌ Quantidade inválida")
    elif choice == '3':
        for i, file in enumerate(csv_files[:10], 1):
            print(f"{i}. {file}")
        indices = input("Números (ex: 1,3,5): ").strip()
        if indices:
            try:
                selected = [csv_files[int(x.strip()) - 1] for x in indices.split(',')
                            if 0 <= int(x.strip()) - 1 < len(csv_files)]
                if selected:
                    _load_and_compare(selected)
            except:
                print("❌ Formato inválido")


def _load_and_compare(file_list):
    """Carrega os arquivos selecionados e chama create_advanced_dashboard."""
    print(f"📊 Carregando {len(file_list)} snapshots...")
    dfs           = []
    snapshot_info = []

    for i, file in enumerate(file_list):
        file_path = os.path.join("data/snapshots", file)
        try:
            df        = pd.read_csv(file_path)
            date_part = file.split('enhanced_')[1].replace('.csv', '')
            date_str  = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]} {date_part[9:11]}:{date_part[11:13]}"
            df['snapshot_period'] = f"Período {i+1} - {date_str}"
            df['snapshot_date']   = date_str
            df['snapshot_index']  = i
            dfs.append(df)
            snapshot_info.append({'file': file, 'date': date_str, 'index': i, 'count': len(df)})
            print(f"✅ {file} ({date_str}) — {len(df)} gems")
        except Exception as e:
            print(f"❌ Erro ao carregar {file}: {e}")

    if dfs:
        create_advanced_dashboard(dfs, snapshot_info)


def show_latest_csv(specific_file=None):
    """Mostra CSV com visualização Plotly — snapshot único com bloco global."""

    if specific_file:
        file_path   = specific_file
        latest_file = os.path.basename(file_path)
    else:
        print("🔍 BUSCANDO CSV MAIS RECENTE...")
        snapshots_dir = "data/snapshots"
        if not os.path.exists(snapshots_dir):
            print("❌ Pasta snapshots não encontrada")
            return
        csv_files = [f for f in os.listdir(snapshots_dir) if f.endswith('.csv') and 'enhanced_' in f]
        if not csv_files:
            print("❌ Nenhum CSV enhanced encontrado")
            return
        csv_files.sort(reverse=True)
        latest_file = csv_files[0]
        file_path   = os.path.join(snapshots_dir, latest_file)

    print(f"📁 Arquivo: {latest_file}")
    print(f"📅 Modificado: {datetime.fromtimestamp(os.path.getmtime(file_path))}")
    print()

    try:
        df = pd.read_csv(file_path)
        print(f"📊 Dados: {len(df)} gems, {len(df.columns)} colunas")
        print()

        changes = df['price_change_percentage_24h'].fillna(0)
        print("📊 ESTATÍSTICAS RÁPIDAS:")
        print("-" * 40)
        print(f"Market Cap Médio: ${df['market_cap'].mean():,.0f}")
        print(f"Volume Total: ${df['total_volume'].fillna(0).sum():,.0f}")
        print(f"Variação 24h Positivas: {(changes > 0).sum()}/{len(changes)} ({(changes > 0).mean()*100:.1f}%)")
        print()

        print("🎨 CRIANDO VISUALIZAÇÃO INTERATIVA (com histórico global)...")
        create_interactive_dashboard(df, latest_file)

    except Exception as e:
        print(f"❌ Erro ao processar CSV: {e}")


def main():
    print("📊 GEMS SYSTEM - VISUALIZADOR INTERATIVO (PLOTLY)")
    print("=" * 60)
    print()

    while True:
        print("Escolha uma opção:")
        print("1. ⭐ Comparar snapshots (DASHBOARD AVANÇADO)")
        print("2. 📊 Ver snapshot mais recente")
        print("3. 📊 Escolher snapshot específico")
        print("4. 📁 Listar todos os CSVs")
        print("0. 🚪 Sair")
        print()

        choice = input("Opção (0-4) [ENTER = 1]: ").strip()

        if choice in ('', '1'):
            show_comparison_snapshots()
        elif choice == '2':
            show_latest_csv()
        elif choice == '3':
            selected_file = show_snapshot_selection()
            if selected_file:
                show_latest_csv(os.path.join("data/snapshots", selected_file))
        elif choice == '4':
            csv_files = get_available_snapshots()
            if csv_files:
                print("📁 CSVs disponíveis:")
                for i, file in enumerate(csv_files[:15], 1):
                    print(f"{i:2d}. {file}")
                print(f"Total: {len(csv_files)} arquivos")
            else:
                print("❌ Nenhum snapshot encontrado")
        elif choice == '0':
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida")
        print()


if __name__ == "__main__":
    main()
