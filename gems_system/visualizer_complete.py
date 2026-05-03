#!/usr/bin/env python3
"""
📊 Visualizador interativo com Plotly + Pandas - Versão Completa
Abre gráficos interativos no navegador - sem servidor!
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
# import numpy as np  # Removido para evitar dependência
from evolution_functions import (
    get_all_snapshots_for_evolution,
    analyze_historical_evolution,
    determine_evolution_status,
    create_evolution_timeline,
    create_hall_of_fame,
    get_evolution_color,
    get_evolution_emoji
)

def create_interactive_dashboard(df, file_name):
    """Cria dashboard interativo com Plotly"""

    # Calcular ratio se não existir
    if 'ratio' not in df.columns:
        df['ratio'] = (df['total_volume'].fillna(0)) / df['market_cap']

    # Criar subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('🏆 Top 15 Market Cap', '📈 Top 15 Volume/MC Ratio',
                       '🚀 Top 15 Variação 24h', '🎯 Top 15 Final Score'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )

    # Top 15 Market Cap
    top_mc = df.nlargest(15, 'market_cap')
    fig.add_trace(
        go.Bar(x=top_mc['symbol'], y=top_mc['market_cap'],
               name='Market Cap', marker_color='#3498db'),
        row=1, col=1
    )

    # Top 15 Volume/MC Ratio
    top_ratio = df.nlargest(15, 'ratio')
    fig.add_trace(
        go.Bar(x=top_ratio['symbol'], y=top_ratio['ratio'],
               name='Volume/MC Ratio', marker_color='#e74c3c'),
        row=1, col=2
    )

    # Top 15 Variação 24h
    top_change = df.nlargest(15, 'price_change_percentage_24h')
    colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in top_change['price_change_percentage_24h']]
    fig.add_trace(
        go.Bar(x=top_change['symbol'], y=top_change['price_change_percentage_24h'],
               name='Variação 24h', marker_color=colors),
        row=2, col=1
    )

    # Top 15 Final Score (se existir)
    if 'final_score' in df.columns:
        top_score = df.nlargest(15, 'final_score')
    else:
        top_score = df.nlargest(15, 'ratio')

    fig.add_trace(
        go.Bar(x=top_score['symbol'], y=top_score['final_score'] if 'final_score' in top_score.columns else top_score['ratio'],
               name='Final Score', marker_color='#f39c12'),
        row=2, col=2
    )

    # Layout
    fig.update_layout(
        title=f'🚀 GEMS SYSTEM DASHBOARD - {file_name}',
        height=800,
        showlegend=False,
        template='plotly_white'
    )

    # Tabela interativa
    fig_table = create_interactive_table(df)

    # HTML completo
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
            .event {{ display: inline-block; margin: 5px; padding: 5px 10px; border-radius: 5px; color: white; }}
            .leader {{ background-color: #e74c3c; }}
            .social {{ background-color: #f39c12; }}
            .rs {{ background-color: #27ae60; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 GEMS SYSTEM DASHBOARD</h1>
            <p><strong>Arquivo:</strong> {file_name}</p>
            <p><strong>Data:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Gems:</strong> {len(df)} | <strong>Colunas:</strong> {len(df.columns)}</p>

            <div class="stats">
                <h3>📊 Estatísticas</h3>
                <p><strong>Market Cap Médio:</strong> ${df['market_cap'].mean():,.0f}</p>
                <p><strong>Volume Total:</strong> ${df['total_volume'].sum():,.0f}</p>
                <p><strong>Variação 24h Positivas:</strong> {(df['price_change_percentage_24h'] > 0).sum()}/{len(df)} ({(df['price_change_percentage_24h'] > 0).mean()*100:.1f}%)</p>
            </div>

            <div id="dashboard"></div>

            <div id="table" style="margin-top: 30px;"></div>
        </div>

        <script>
            {fig.to_html(div_id="dashboard", include_plotlyjs=False)}
            {fig_table.to_html(div_id="table", include_plotlyjs=False)}
        </script>
    </body>
    </html>
    """

    # Criar arquivo temporário
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_content)
        temp_file = f.name

    print("🌐 Abrindo visualização no navegador...")

    # Abrir no navegador
    webbrowser.open(f'file://{temp_file}')

    # Fechar e apagar após alguns segundos
    import threading
    import time

    def cleanup():
        time.sleep(5)  # Esperar 5 segundos para abrir
        try:
            os.unlink(temp_file)
        except:
            pass

    cleanup_thread = threading.Thread(target=cleanup)
    cleanup_thread.daemon = True
    cleanup_thread.start()

    return df

def create_interactive_table(df):
    """Cria tabela interativa com todas as colunas"""

    # Preparar colunas para exibição
    display_cols = ['symbol', 'name', 'market_cap', 'total_volume', 'price_change_percentage_24h']

    # Adicionar colunas de score se existirem
    if 'ratio' in df.columns:
        display_cols.append('ratio')
    if 'final_score' in df.columns:
        display_cols.append('final_score')

    # Adicionar colunas de persistência se existirem
    if 'persistence_count_3d' in df.columns:
        display_cols.extend(['persistence_count_3d', 'persistence_count_7d', 'persistence_count_14d'])

    # Adicionar colunas de liderança se existirem
    if 'timeframe_classification' in df.columns:
        display_cols.extend(['timeframe_classification'])
    if 'is_confirmed_leader' in df.columns:
        display_cols.extend(['is_confirmed_leader'])

    # Adicionar colunas de análise técnica
    if 'zone' in df.columns:
        display_cols.extend(['zone'])
    if 'momentum' in df.columns:
        display_cols.extend(['momentum'])
    if 'is_gold' in df.columns:
        display_cols.extend(['is_gold'])
    if 'rs_strong' in df.columns:
        display_cols.extend(['rs_strong'])

    # Filtrar colunas existentes
    table_df = df[[col for col in display_cols if col in df.columns]].copy()

    # Formatar colunas
    table_df['market_cap'] = table_df['market_cap'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else 'N/A')
    table_df['total_volume'] = table_df['total_volume'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else 'N/A')
    table_df['price_change_percentage_24h'] = table_df['price_change_percentage_24h'].apply(
        lambda x: f"{x:.1f}%" if pd.notna(x) else 'N/A'
    )

    if 'ratio' in table_df.columns:
        table_df['ratio'] = table_df['ratio'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')

    if 'final_score' in table_df.columns:
        table_df['final_score'] = table_df['final_score'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')

    # Formatar contadores de persistência
    if 'persistence_count_3d' in table_df.columns:
        table_df['persistence_count_3d'] = table_df['persistence_count_3d'].apply(lambda x: f"{x}x")
        table_df['persistence_count_7d'] = table_df['persistence_count_7d'].apply(lambda x: f"{x}x")
        table_df['persistence_count_14d'] = table_df['persistence_count_14d'].apply(lambda x: f"{x}x")

    # Formatar colunas de liderança
    if 'timeframe_classification' in table_df.columns:
        table_df['timeframe_classification'] = table_df['timeframe_classification'].apply(
            lambda x: x.replace('_', ' ').title() if pd.notna(x) else 'Unknown'
        )
    if 'is_confirmed_leader' in table_df.columns:
        table_df['is_confirmed_leader'] = table_df['is_confirmed_leader'].apply(
            lambda x: '👑 YES' if x else '❌ NO'
        )

    # Formatar colunas de análise técnica
    if 'zone' in table_df.columns:
        table_df['zone'] = table_df['zone'].apply(
            lambda x: (
                f"🔥 {x.replace('_', ' ').title()}" if x == 'breakout' else
                f"🟠 {x.replace('_', ' ').title()}" if x == 'strong' else
                f"🟡 {x.replace('_', ' ').title()}" if x == 'early_accumulation' else
                f"⚪ {x.replace('_', ' ').title()}"
            ) if pd.notna(x) else 'Unknown'
        )
    if 'momentum' in table_df.columns:
        table_df['momentum'] = table_df['momentum'].apply(
            lambda x: f"{'🔥 High' if x == 'high' else '📈 Medium' if x == 'medium' else '📊 Low'}" if pd.notna(x) else 'Unknown'
        )
    if 'is_gold' in table_df.columns:
        table_df['is_gold'] = table_df['is_gold'].apply(
            lambda x: '👑 Gold' if x else '⚪ Normal'
        )
    if 'rs_strong' in table_df.columns:
        table_df['rs_strong'] = table_df['rs_strong'].apply(
            lambda x: '💪 Strong' if x else '⚪ Normal'
        )

    # Renomear colunas para exibição
    column_mapping = {
        'symbol': 'Symbol',
        'name': 'Name',
        'market_cap': 'Market Cap',
        'total_volume': 'Volume',
        'price_change_percentage_24h': '24h%',
        'ratio': 'Ratio',
        'final_score': 'Score',
        'persistence_count_3d': '3d',
        'persistence_count_7d': '7d',
        'persistence_count_14d': '14d',
        'timeframe_classification': 'Classification',
        'is_confirmed_leader': 'Leader',
        'zone': 'Zone',
        'momentum': 'Momentum',
        'is_gold': 'Gold',
        'rs_strong': 'RS'
    }

    table_df.rename(columns=column_mapping, inplace=True)

    # Criar tabela Plotly
    fig_table = go.Figure(data=[go.Table(
        header=dict(
            values=list(table_df.columns),
            fill_color='#3498db',
            align='left',
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[table_df[col] for col in table_df.columns],
            fill_color='lavender',
            align='left',
            font=dict(color='black', size=11)
        )
    )])

    fig_table.update_layout(
        title="📊 DADOS COMPLETOS",
        title_x=0.5,
        height=600,
        template='plotly_white'
    )

    return fig_table

def get_available_snapshots():
    """Retorna lista de snapshots enhanced disponíveis ordenados por data"""
    snapshots_dir = "data/snapshots"
    if not os.path.exists(snapshots_dir):
        return []

    # Filtrar apenas arquivos enhanced (com dados completos)
    csv_files = [f for f in os.listdir(snapshots_dir)
                 if f.endswith('.csv') and 'enhanced_' in f]
    csv_files.sort(reverse=True)  # Mais recente primeiro
    return csv_files

def show_snapshot_selection():
    """Mostra menu de seleção de snapshots"""
    csv_files = get_available_snapshots()

    if not csv_files:
        print("❌ Nenhum snapshot encontrado")
        return None

    print("📁 Snapshots disponíveis:")
    print("0. 📊 Mais recente (automático)")

    for i, file in enumerate(csv_files[:10], 1):
        # Extrair data do nome do arquivo enhanced
        try:
            date_part = file.split('enhanced_')[1].replace('.csv', '')
            date_str = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]} {date_part[9:11]}:{date_part[11:13]}"
            print(f"{i:2d}. {file} ({date_str})")
        except:
            print(f"{i:2d}. {file}")

    print()

    while True:
        try:
            choice = input(f"Escolha snapshot (0-{min(len(csv_files), 10)}): ").strip()

            if choice == '0':
                return csv_files[0]  # Mais recente
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
    """Mostra comparação entre múltiplos snapshots"""
    csv_files = get_available_snapshots()

    if len(csv_files) < 2:
        print("❌ Precisa de pelo menos 2 snapshots para comparar")
        return

    print("📊 COMPARAÇÃO DE SNAPSHOTS:")
    print("1. ⭐ Avançado (abas) - últimos 2 snapshots")
    print("2. ⭐ Avançado (abas) - escolher quantidade (2-10)")
    print("3. ⭐ Avançado (abas) - escolher snapshots específicos")
    print("4. 📈 Lado a lado (legado) - últimos 2 snapshots")
    print("5. 📈 Lado a lado (legado) - escolher snapshots específicos")
    print("0. ⬅️ Voltar")
    print()

    choice = input("Opção (0-5): ").strip()

    if choice == '1' or choice == '':
        show_advanced_comparison(csv_files[:2])

    elif choice == '2':
        qty_str = input("Quantidade de snapshots (2-10): ").strip()
        try:
            qty = int(qty_str)
            if qty < 2:
                qty = 2
            if qty > 10:
                qty = 10
            show_advanced_comparison(csv_files[:qty])
        except:
            print("❌ Quantidade inválida")

    elif choice == '3':
        print("Escolha os snapshots (separados por vírgula):")
        for i, file in enumerate(csv_files[:10], 1):
            print(f"{i}. {file}")

        indices = input("Números (ex: 1,3,5): ").strip()
        if indices:
            try:
                selected_indices = [int(x.strip()) - 1 for x in indices.split(',')]
                selected_files = [csv_files[i] for i in selected_indices if 0 <= i < len(csv_files)]
                if selected_files:
                    show_advanced_comparison(selected_files)
            except:
                print("❌ Formato inválido")

    elif choice == '4':
        show_multiple_snapshots(csv_files[:2])

    elif choice == '5':
        print("Escolha os snapshots (separados por vírgula):")
        for i, file in enumerate(csv_files[:10], 1):
            print(f"{i}. {file}")

        indices = input("Números (ex: 1,3,5): ").strip()
        if indices:
            try:
                selected_indices = [int(x.strip()) - 1 for x in indices.split(',')]
                selected_files = [csv_files[i] for i in selected_indices if 0 <= i < len(csv_files)]
                if selected_files:
                    show_multiple_snapshots(selected_files)
            except:
                print("❌ Formato inválido")

def show_multiple_snapshots(file_list):
    """Mostra múltiplos snapshots em comparação separada por período"""
    print(f"📊 Carregando {len(file_list)} snapshots para comparação...")

    dfs = []
    snapshot_info = []

    for i, file in enumerate(file_list):
        file_path = os.path.join("data/snapshots", file)
        try:
            df = pd.read_csv(file_path)

            # Extrair data/hora do arquivo
            date_part = file.split('enhanced_')[1].replace('.csv', '')
            date_str = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]} {date_part[9:11]}:{date_part[11:13]}"

            # Adicionar informações do período
            df['snapshot_period'] = f"Período {i+1} - {date_str}"
            df['snapshot_date'] = date_str
            df['snapshot_index'] = i

            dfs.append(df)
            snapshot_info.append({
                'file': file,
                'date': date_str,
                'index': i,
                'count': len(df)
            })
            print(f"✅ {file} ({date_str}) - {len(df)} gems")
        except Exception as e:
            print(f"❌ Erro ao carregar {file}: {e}")

    if not dfs:
        print("❌ Nenhum snapshot carregado")
        return

    print()
    print("📊 RESUMO DOS PERÍODOS:")
    print("-" * 50)
    for info in snapshot_info:
        print(f"Período {info['index']+1}: {info['date']} ({info['count']} gems)")
    print()

    # Criar dashboard comparativo
    create_comparison_dashboard(dfs, snapshot_info)

def create_comparison_dashboard(dfs, snapshot_info):
    """Cria dashboard comparativo com snapshots separados"""

    # Combinar dados mantendo separação
    combined_df = pd.concat(dfs, ignore_index=True)

    # Criar subplots para comparação
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('🏆 Market Cap por Período', '📈 Volume/MC Ratio por Período',
                       '🚀 Variação 24h por Período', '🎯 Score por Período'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )

    # Cores diferentes para cada período
    colors = ['#3498db', '#e74c3c', '#f39c12', '#27ae60', '#9b59b6']

    # Market Cap por período
    for i, df in enumerate(dfs):
        top_mc = df.nlargest(10, 'market_cap')  # Top 10 por período
        fig.add_trace(
            go.Bar(
                x=top_mc['symbol'],
                y=top_mc['market_cap'],
                name=f'MC - {snapshot_info[i]["date"]}',
                marker_color=colors[i % len(colors)],
                legendgroup=f'period_{i}'
            ),
            row=1, col=1
        )

    # Volume/MC Ratio por período
    for i, df in enumerate(dfs):
        top_ratio = df.nlargest(10, 'ratio')
        fig.add_trace(
            go.Bar(
                x=top_ratio['symbol'],
                y=top_ratio['ratio'],
                name=f'Ratio - {snapshot_info[i]["date"]}',
                marker_color=colors[i % len(colors)],
                legendgroup=f'period_{i}'
            ),
            row=1, col=2
        )

    # Variação 24h por período
    for i, df in enumerate(dfs):
        top_change = df.nlargest(10, 'price_change_percentage_24h')
        change_colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in top_change['price_change_percentage_24h']]
        fig.add_trace(
            go.Bar(
                x=top_change['symbol'],
                y=top_change['price_change_percentage_24h'],
                name=f'24h - {snapshot_info[i]["date"]}',
                marker_color=change_colors,
                legendgroup=f'period_{i}'
            ),
            row=2, col=1
        )

    # Score por período
    for i, df in enumerate(dfs):
        if 'final_score' in df.columns:
            top_score = df.nlargest(10, 'final_score')
        else:
            top_score = df.nlargest(10, 'ratio')

        fig.add_trace(
            go.Bar(
                x=top_score['symbol'],
                y=top_score['final_score'] if 'final_score' in top_score.columns else top_score['ratio'],
                name=f'Score - {snapshot_info[i]["date"]}',
                marker_color=colors[i % len(colors)],
                legendgroup=f'period_{i}'
            ),
            row=2, col=2
        )

    # Layout comparativo
    fig.update_layout(
        title=f'📊 COMPARATIVO DE SNAPSHOTS - {" vs ".join([info["date"] for info in snapshot_info])}',
        height=900,
        showlegend=True,
        template='plotly_white',
        hovermode='x unified'
    )

    # Tabela comparativa com separação por período
    fig_table = create_comparison_table(combined_df, snapshot_info)

    # HTML completo com design melhorado
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>📊 GEMS SYSTEM - COMPARATIVO DE SNAPSHOTS</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; text-align: center; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            .period-summary {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .period-item {{ margin: 10px 0; padding: 10px; border-left: 4px solid #3498db; background-color: white; }}
            .period-0 {{ border-left-color: #3498db; }}
            .period-1 {{ border-left-color: #e74c3c; }}
            .period-2 {{ border-left-color: #f39c12; }}
            .stats {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 GEMS SYSTEM - COMPARATIVO DE SNAPSHOTS</h1>

            <div class="period-summary">
                <h3>📅 Períodos Comparados</h3>
                {''.join([f'<div class="period-item period-{info["index"]}"><strong>Período {info["index"]+1}:</strong> {info["date"]} ({info["count"]} gems)</div>' for info in snapshot_info])}
            </div>

            <div class="stats">
                <h3>📊 Estatísticas Combinadas</h3>
                <p><strong>Total de Gems:</strong> {len(combined_df)} (com duplicatas entre períodos)</p>
                <p><strong>Períodos:</strong> {len(snapshot_info)}</p>
                <p><strong>Market Cap Médio Geral:</strong> ${combined_df['market_cap'].mean():,.0f}</p>
                <p><strong>Volume Total Geral:</strong> ${combined_df['total_volume'].sum():,.0f}</p>
            </div>

            <div id="dashboard"></div>

            <div id="table" style="margin-top: 30px;"></div>
        </div>

        <script>
            {fig.to_html(div_id="dashboard", include_plotlyjs=False)}
            {fig_table.to_html(div_id="table", include_plotlyjs=False)}
        </script>
    </body>
    </html>
    """

    # Criar arquivo temporário
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_content)
        temp_file = f.name

    print("🌐 Abrindo visualização comparativa no navegador...")

    # Abrir no navegador
    webbrowser.open(f'file://{temp_file}')

    # Limpar após alguns segundos
    import threading
    import time

    def cleanup():
        time.sleep(5)
        try:
            os.unlink(temp_file)
        except:
            pass

    cleanup_thread = threading.Thread(target=cleanup)
    cleanup_thread.daemon = True
    cleanup_thread.start()

def create_comparison_table(df, snapshot_info):
    """Cria tabela comparativa com separação por período"""

    # Preparar colunas para exibição
    display_cols = ['snapshot_period', 'symbol', 'name', 'market_cap', 'total_volume', 'price_change_percentage_24h']

    # Adicionar colunas de score se existirem
    if 'ratio' in df.columns:
        display_cols.append('ratio')
    if 'final_score' in df.columns:
        display_cols.append('final_score')

    # Adicionar colunas de persistência se existirem
    if 'persistence_count_3d' in df.columns:
        display_cols.extend(['persistence_count_3d', 'persistence_count_7d', 'persistence_count_14d'])

    # Adicionar colunas de liderança se existirem
    if 'timeframe_classification' in df.columns:
        display_cols.extend(['timeframe_classification'])
    if 'is_confirmed_leader' in df.columns:
        display_cols.extend(['is_confirmed_leader'])

    # Adicionar colunas de análise técnica
    if 'zone' in df.columns:
        display_cols.extend(['zone'])
    if 'momentum' in df.columns:
        display_cols.extend(['momentum'])
    if 'is_gold' in df.columns:
        display_cols.extend(['is_gold'])
    if 'rs_strong' in df.columns:
        display_cols.extend(['rs_strong'])

    # Filtrar colunas existentes
    table_df = df[[col for col in display_cols if col in df.columns]].copy()

    # Ordenar por período e depois por score/ratio
    if 'final_score' in table_df.columns:
        table_df = table_df.sort_values(['snapshot_period', 'final_score'], ascending=[True, False])
    elif 'ratio' in table_df.columns:
        table_df = table_df.sort_values(['snapshot_period', 'ratio'], ascending=[True, False])

    # Formatar colunas
    table_df['market_cap'] = table_df['market_cap'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else 'N/A')
    table_df['total_volume'] = table_df['total_volume'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else 'N/A')
    table_df['price_change_percentage_24h'] = table_df['price_change_percentage_24h'].apply(
        lambda x: f"{x:.1f}%" if pd.notna(x) else 'N/A'
    )

    if 'ratio' in table_df.columns:
        table_df['ratio'] = table_df['ratio'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')

    if 'final_score' in table_df.columns:
        table_df['final_score'] = table_df['final_score'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')

    # Formatar contadores de persistência
    if 'persistence_count_3d' in table_df.columns:
        table_df['persistence_count_3d'] = table_df['persistence_count_3d'].apply(lambda x: f"{x}x")
        table_df['persistence_count_7d'] = table_df['persistence_count_7d'].apply(lambda x: f"{x}x")
        table_df['persistence_count_14d'] = table_df['persistence_count_14d'].apply(lambda x: f"{x}x")

    # Formatar colunas de liderança
    if 'timeframe_classification' in table_df.columns:
        table_df['timeframe_classification'] = table_df['timeframe_classification'].apply(
            lambda x: x.replace('_', ' ').title() if pd.notna(x) else 'Unknown'
        )
    if 'is_confirmed_leader' in table_df.columns:
        table_df['is_confirmed_leader'] = table_df['is_confirmed_leader'].apply(
            lambda x: '👑 YES' if x else '❌ NO'
        )

    # Formatar colunas de análise técnica
    if 'zone' in table_df.columns:
        table_df['zone'] = table_df['zone'].apply(
            lambda x: (
                f"🔥 {x.replace('_', ' ').title()}" if x == 'breakout' else
                f"🟠 {x.replace('_', ' ').title()}" if x == 'strong' else
                f"🟡 {x.replace('_', ' ').title()}" if x == 'early_accumulation' else
                f"⚪ {x.replace('_', ' ').title()}"
            ) if pd.notna(x) else 'Unknown'
        )
    if 'momentum' in table_df.columns:
        table_df['momentum'] = table_df['momentum'].apply(
            lambda x: f"{'🔥 High' if x == 'high' else '📈 Medium' if x == 'medium' else '📊 Low'}" if pd.notna(x) else 'Unknown'
        )
    if 'is_gold' in table_df.columns:
        table_df['is_gold'] = table_df['is_gold'].apply(
            lambda x: '👑 Gold' if x else '⚪ Normal'
        )
    if 'rs_strong' in table_df.columns:
        table_df['rs_strong'] = table_df['rs_strong'].apply(
            lambda x: '💪 Strong' if x else '⚪ Normal'
        )

    # Renomear colunas para exibição
    column_mapping = {
        'snapshot_period': 'Período',
        'symbol': 'Symbol',
        'name': 'Name',
        'market_cap': 'Market Cap',
        'total_volume': 'Volume',
        'price_change_percentage_24h': '24h%',
        'ratio': 'Ratio',
        'final_score': 'Score',
        'persistence_count_3d': '3d',
        'persistence_count_7d': '7d',
        'persistence_count_14d': '14d',
        'timeframe_classification': 'Classification',
        'is_confirmed_leader': 'Leader',
        'zone': 'Zone',
        'momentum': 'Momentum',
        'is_gold': 'Gold',
        'rs_strong': 'RS'
    }

    table_df.rename(columns=column_mapping, inplace=True)

    # Cores diferentes para cada período na tabela
    colors = ['#3498db', '#e74c3c', '#f39c12', '#27ae60', '#9b59b6']

    # Criar células com cores por período
    cell_colors = []
    for col in table_df.columns:
        if col == 'Período':
            # Cores diferentes para cada período
            period_colors = []
            for period in table_df['Período']:
                for i, info in enumerate(snapshot_info):
                    if f"Período {i+1}" in str(period):
                        period_colors.append(colors[i % len(colors)])
                        break
                else:
                    period_colors.append('#ecf0f1')
            cell_colors.append(period_colors)
        else:
            # Cor padrão para outras colunas
            cell_colors.append(['lavender'] * len(table_df))

    # Criar tabela Plotly comparativa
    fig_table = go.Figure(data=[go.Table(
        header=dict(
            values=list(table_df.columns),
            fill_color='#3498db',
            align='left',
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[table_df[col] for col in table_df.columns],
            fill_color=cell_colors,
            align='left',
            font=dict(color='black', size=11)
        )
    )])

    fig_table.update_layout(
        title="📊 COMPARATIVO DE SNAPSHOTS - DADOS SEPARADOS POR PERÍODO",
        title_x=0.5,
        height=800,
        template='plotly_white'
    )

    return fig_table

def show_advanced_comparison(file_list):
    """Mostra comparação avançada com abas separadas e filtros interativos"""
    print(f"📊 Carregando {len(file_list)} snapshots para comparação avançada...")

    dfs = []
    snapshot_info = []

    for i, file in enumerate(file_list):
        file_path = os.path.join("data/snapshots", file)
        try:
            df = pd.read_csv(file_path)

            # Extrair data/hora do arquivo
            date_part = file.split('enhanced_')[1].replace('.csv', '')
            date_str = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]} {date_part[9:11]}:{date_part[11:13]}"

            # Adicionar informações do período
            df['snapshot_period'] = f"Período {i+1} - {date_str}"
            df['snapshot_date'] = date_str
            df['snapshot_index'] = i

            dfs.append(df)
            snapshot_info.append({
                'file': file,
                'date': date_str,
                'index': i,
                'count': len(df)
            })
            print(f"✅ {file} ({date_str}) - {len(df)} gems")
        except Exception as e:
            print(f"❌ Erro ao carregar {file}: {e}")

    if not dfs:
        print("❌ Nenhum snapshot carregado")
        return

    print()
    print("📊 RESUMO DOS PERÍODOS:")
    print("-" * 50)
    for info in snapshot_info:
        print(f"Período {info['index']+1}: {info['date']} ({info['count']} gems)")
    print()

    # Adicionar score_change para cada crypto (diferença entre primeiro e último período)
    if len(dfs) >= 2:
        first_df = dfs[0]
        last_df = dfs[-1]

        # Criar dicionário de scores do primeiro período
        first_scores = dict(zip(first_df['symbol'], first_df['final_score']))

        # Adicionar score_change ao último DataFrame
        score_changes = []
        for _, row in last_df.iterrows():
            symbol = row['symbol']
            current_score = row['final_score']
            first_score = first_scores.get(symbol, 0)
            score_change = current_score - first_score
            score_changes.append(score_change)

        last_df = last_df.copy()
        last_df['score_change'] = score_changes
        dfs[-1] = last_df

    # Criar dashboard avançado com abas
    create_advanced_dashboard(dfs, snapshot_info)

def create_advanced_dashboard(dfs, snapshot_info):
    """Cria dashboard avançado com abas separadas e filtros"""

    # Criar gráfico TOP 10 comparativo
    top10_comparison = create_top10_comparison_chart(dfs, snapshot_info)

    # Criar HTML com abas e filtros
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
            .top-comparison {{ background-color: #ecf0f1; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
            .tabs {{ display: flex; border-bottom: 2px solid #3498db; margin-bottom: 20px; }}
            .tab {{ padding: 12px 20px; cursor: pointer; border: none; background: #ecf0f1; margin-right: 5px; border-radius: 5px 5px 0 0; }}
            .tab.active {{ background: #3498db; color: white; }}
            .tab-content {{ display: none; }}
            .tab-content.active {{ display: block; }}
            .filters {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            .filter-item {{ margin: 10px 0; }}
            .stats {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .period-summary {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .period-item {{ margin: 10px 0; padding: 10px; border-left: 4px solid #3498db; background-color: white; }}
            .period-0 {{ border-left-color: #3498db; }}
            .period-1 {{ border-left-color: #e74c3c; }}
            .period-2 {{ border-left-color: #f39c12; }}
            .ranking-change {{ font-weight: bold; }}
            .rank-up {{ color: #27ae60; }}
            .rank-down {{ color: #e74c3c; }}
            .rank-same {{ color: #95a5a6; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 GEMS SYSTEM - COMPARATIVO AVANÇADO</h1>

            <div class="top-comparison">
                <h3>📈 EVOLUÇÃO TEMPORAL - TOP 5 CRYPTOS</h3>
                <div id="top10-comparison-chart"></div>

                <div id="evolution-chart" style="margin-top: 30px;"></div>

                <div id="ranking-summary" style="margin-top: 20px;"></div>

                <!-- 🚀 NOVOS COMPONENTES EVOLUTIVOS -->
                <div id="hall-of-fame" style="margin-top: 20px;"></div>
            </div>

            <div class="period-summary">
                <h3>📅 Períodos Comparados</h3>
                {''.join([f'<div class="period-item period-{info["index"]}"><strong>Período {info["index"]+1}:</strong> {info["date"]} ({info["count"]} gems)</div>' for info in snapshot_info])}
            </div>

            <div class="filters">
                <h3>🔍 Filtros Interativos</h3>
                <div class="filter-item">
                    <label>Filtrar por Symbol:</label>
                    <input type="text" id="symbolFilter" placeholder="Digite o symbol (ex: BTC)" onkeyup="filterData()">
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

            <div class="tabs">
                <button class="tab active" onclick="showTab(0)">Período 1 - {snapshot_info[0]["date"]}</button>
                <button class="tab" onclick="showTab(1)">Período 2 - {snapshot_info[1]["date"] if len(snapshot_info) > 1 else "N/A"}</button>
            </div>

            <div id="tab-0" class="tab-content active">
                {create_period_html(dfs[0], snapshot_info[0], 0)}
            </div>
            <div id="tab-1" class="tab-content">
                {create_period_html(dfs[1], snapshot_info[1], 1) if len(dfs) > 1 else "<p>Nenhum dado disponível</p>"}
            </div>
        </div>

        <script>
            {top10_comparison}

            function showTab(tabIndex) {{
                // Esconder todos os conteúdos
                const contents = document.querySelectorAll('.tab-content');
                contents.forEach(content => content.classList.remove('active'));

                // Remover active de todas as abas
                const tabs = document.querySelectorAll('.tab');
                tabs.forEach(tab => tab.classList.remove('active'));

                // Mostrar conteúdo selecionado
                const target = document.getElementById('tab-' + tabIndex);
                if (target) {{
                    target.classList.add('active');
                }}

                // Adicionar active à aba selecionada
                if (tabs[tabIndex]) {{
                    tabs[tabIndex].classList.add('active');
                }}
            }}

            window.showTab = showTab;

            function filterData() {{
                const symbolFilter = document.getElementById('symbolFilter').value.toUpperCase();
                const scoreFilter = parseFloat(document.getElementById('scoreFilter').value) || 0;
                const mcFilter = parseFloat(document.getElementById('mcFilter').value) || 0;
                const showFilter = document.getElementById('showFilter').value;

                // Aplicar filtros a todas as tabelas
                for (let i = 0; i < {len(dfs)}; i++) {{
                    const table = document.querySelector('#tab-' + i + ' table');
                    if (table) {{
                        const rows = table.getElementsByTagName('tr');
                        for (let row of rows) {{
                            if (row.rowIndex === 0) continue; // Pular header

                            const cells = row.getElementsByTagName('td');
                            const symbol = cells[1] ? cells[1].textContent.toUpperCase() : '';
                            const score = cells[5] ? parseFloat(cells[5].textContent) : 0;
                            const mc = cells[3] ? parseFloat(cells[3].textContent.replace(/[$,]/g, '')) : 0;

                            let show = true;
                            if (symbolFilter && !symbol.includes(symbolFilter)) show = false;
                            if (score < scoreFilter) show = false;
                            if (mc < mcFilter) show = false;

                            row.style.display = show ? '' : 'none';
                        }}
                    }}
                }}
            }}
        </script>
    </body>
    </html>
    """

    # Criar arquivo temporário
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_content)
        temp_file = f.name

    print("🌐 Abrindo visualização avançada no navegador...")

    # Abrir no navegador
    webbrowser.open(f'file://{temp_file}')

    # Limpar após alguns segundos
    import threading
    import time

    def cleanup():
        time.sleep(5)
        try:
            os.unlink(temp_file)
        except:
            pass

    cleanup_thread = threading.Thread(target=cleanup)
    cleanup_thread.daemon = True
    cleanup_thread.start()

def create_top10_comparison_chart(dfs, snapshot_info):
    """Cria gráfico comparativo TOP 10 unificado com ranking e análises avançadas - Versão Evolutiva Completa"""

    # Coletar TODOS os snapshots disponíveis para análise evolutiva
    all_snapshots_data = get_all_snapshots_for_evolution()

    # DFS globais (histórico completo) para gráficos/estatísticas gerais
    global_dfs = [s['df'] for s in all_snapshots_data if isinstance(s, dict) and 'df' in s]

    # Coletar dados dos snapshots selecionados (recorte atual - usado abaixo em "Períodos Comparados")
    all_crypto_data = {}

    for i, df in enumerate(dfs):
        # Ordenar por score ou ratio
        if 'final_score' in df.columns:
            sorted_df = df.sort_values('final_score', ascending=False)
            score_col = 'final_score'
        elif 'ratio' in df.columns:
            sorted_df = df.sort_values('ratio', ascending=False)
            score_col = 'ratio'
        else:
            sorted_df = df.sort_values('market_cap', ascending=False)
            score_col = 'market_cap'

        # Pegar top 20 para garantir material para análise
        top_crypto = sorted_df.head(20)

        for _, row in top_crypto.iterrows():
            symbol = row['symbol']
            score = row[score_col] if pd.notna(row[score_col]) else 0
            mc = row['market_cap'] if pd.notna(row['market_cap']) else 0
            volume = row['total_volume'] if pd.notna(row['total_volume']) else 0
            change_24h = row['price_change_percentage_24h'] if pd.notna(row['price_change_percentage_24h']) else 0

            # Adicionar setor/categoria se disponível
            sector = row.get('sector', 'Unknown')
            category = row.get('category', row.get('timeframe_classification', 'Unknown'))

            if symbol not in all_crypto_data:
                all_crypto_data[symbol] = {
                    'scores': [],
                    'mcs': [],
                    'volumes': [],
                    'changes_24h': [],
                    'periods_present': [],
                    'total_periods': len(dfs),
                    'sector': sector,
                    'category': category
                }

            all_crypto_data[symbol]['scores'].append(score)
            all_crypto_data[symbol]['mcs'].append(mc)
            all_crypto_data[symbol]['volumes'].append(volume)
            all_crypto_data[symbol]['changes_24h'].append(change_24h)
            all_crypto_data[symbol]['periods_present'].append(i)

    # Adicionar dados históricos completos
    historical_data = analyze_historical_evolution(all_snapshots_data, dfs)

    # ===== VISÃO GLOBAL (histórico completo) =====
    global_crypto_data = {}
    for i, df in enumerate(global_dfs):
        # Ordenar por score ou ratio
        if 'final_score' in df.columns:
            sorted_df = df.sort_values('final_score', ascending=False)
            score_col = 'final_score'
        elif 'ratio' in df.columns:
            sorted_df = df.sort_values('ratio', ascending=False)
            score_col = 'ratio'
        else:
            sorted_df = df.sort_values('market_cap', ascending=False)
            score_col = 'market_cap'

        top_crypto = sorted_df.head(20)

        for _, row in top_crypto.iterrows():
            symbol = row.get('symbol')
            if not symbol:
                continue

            score = row[score_col] if pd.notna(row[score_col]) else 0
            mc = row['market_cap'] if pd.notna(row.get('market_cap')) else 0
            volume = row['total_volume'] if pd.notna(row.get('total_volume')) else 0
            change_24h = row['price_change_percentage_24h'] if pd.notna(row.get('price_change_percentage_24h')) else 0

            sector = row.get('sector', 'Unknown')
            category = row.get('category', row.get('timeframe_classification', 'Unknown'))

            if symbol not in global_crypto_data:
                global_crypto_data[symbol] = {
                    'scores': [],
                    'mcs': [],
                    'volumes': [],
                    'changes_24h': [],
                    'periods_present': [],
                    'total_periods': len(global_dfs) if global_dfs else 0,
                    'sector': sector,
                    'category': category
                }

            global_crypto_data[symbol]['scores'].append(score)
            global_crypto_data[symbol]['mcs'].append(mc)
            global_crypto_data[symbol]['volumes'].append(volume)
            global_crypto_data[symbol]['changes_24h'].append(change_24h)
            global_crypto_data[symbol]['periods_present'].append(i)

    global_crypto_ranking = []
    for symbol, data in global_crypto_data.items():
        avg_score = sum(data['scores']) / len(data['scores']) if data['scores'] else 0
        consistency = (len(data['periods_present']) / data['total_periods']) if data['total_periods'] else 0
        avg_mc = sum(data['mcs']) / len(data['mcs']) if data['mcs'] else 0
        avg_volume = sum(data['volumes']) / len(data['volumes']) if data['volumes'] else 0
        avg_change = sum(data['changes_24h']) / len(data['changes_24h']) if data['changes_24h'] else 0

        if len(data['scores']) > 1:
            mean_score = sum(data['scores']) / len(data['scores'])
            variance = sum((x - mean_score) ** 2 for x in data['scores']) / len(data['scores'])
            score_volatility = variance ** 0.5
        else:
            score_volatility = 0

        evolution_status = determine_evolution_status(symbol, historical_data, data['periods_present'])

        first_period = 0 in data['periods_present']
        last_period = (len(global_dfs) - 1) in data['periods_present'] if global_dfs else False

        if consistency == 1.0:
            presence_type = 'consistent'
        elif first_period and not last_period:
            presence_type = 'gone'
        elif not first_period and last_period:
            presence_type = 'new'
        else:
            presence_type = 'intermittent'

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

    global_crypto_ranking.sort(key=lambda x: (x['avg_score'], x['consistency'], x['avg_mc']), reverse=True)

    # Calcular métricas avançadas
    crypto_ranking = []
    for symbol, data in all_crypto_data.items():
        avg_score = sum(data['scores']) / len(data['scores'])
        consistency = len(data['periods_present']) / data['total_periods']
        avg_mc = sum(data['mcs']) / len(data['mcs'])
        avg_volume = sum(data['volumes']) / len(data['volumes'])
        avg_change = sum(data['changes_24h']) / len(data['changes_24h'])

        # Calcular volatilidade (desvio padrão dos scores) - sem numpy
        if len(data['scores']) > 1:
            mean_score = sum(data['scores']) / len(data['scores'])
            variance = sum((x - mean_score) ** 2 for x in data['scores']) / len(data['scores'])
            score_volatility = variance ** 0.5
        else:
            score_volatility = 0

        # Determinar status evolutivo
        evolution_status = determine_evolution_status(symbol, historical_data, data['periods_present'])

        # Determinar tipo de presença
        first_period = 0 in data['periods_present']
        last_period = (len(dfs) - 1) in data['periods_present']

        if consistency == 1.0:
            presence_type = 'consistent'
        elif first_period and not last_period:
            presence_type = 'gone'
        elif not first_period and last_period:
            presence_type = 'new'
        else:
            presence_type = 'intermittent'

        crypto_ranking.append({
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

    # Ordenar por score médio (com critérios de desempate)
    crypto_ranking.sort(key=lambda x: (x['avg_score'], x['consistency'], x['avg_mc']), reverse=True)

    # Pegar TOP 15 (visão global)
    top15_global = global_crypto_ranking[:15]

    # Criar todos os gráficos e resumos (visão global) - tudo acima de "Períodos Comparados"
    charts_js = create_all_comparison_charts(top15_global, snapshot_info, global_crypto_ranking, global_dfs if global_dfs else dfs, historical_data)
    summary_html = create_advanced_summary_table(top15_global, global_crypto_ranking, len(global_dfs) if global_dfs else len(dfs), historical_data, dfs[-1] if len(dfs) > 0 else None)

    # Adicionar crypto_ranking e global_dfs ao historical_data para o Hall da Fama e tendências (visão global)
    historical_data['crypto_ranking'] = global_crypto_ranking
    historical_data['global_dfs'] = global_dfs

    # Criar Hall das Saídas
    hall_of_fame_html = create_hall_of_fame(historical_data, snapshot_info)

    # Retornar JavaScript completo
    return f"""
        {charts_js}

        // Adicionar resumo avançado
        document.getElementById('ranking-summary').innerHTML = `{summary_html.replace('`', '\\`')}`;

        // Adicionar Hall da Fama
        document.getElementById('hall-of-fame').innerHTML = `{hall_of_fame_html.replace('`', '\\`')}`;
    """

def _fig_to_plotly_newplot_js(fig, div_id: str) -> str:
    fig_json = fig.to_plotly_json()
    data_json = json.dumps(fig_json.get('data', []), ensure_ascii=False)
    layout_json = json.dumps(fig_json.get('layout', {}), ensure_ascii=False)
    return (
        f"Plotly.newPlot('{div_id}', {data_json}, {layout_json}, {{responsive: true}});"
    )

def create_all_comparison_charts(top10, snapshot_info, crypto_ranking, dfs, historical_data=None):
    """Cria todos os gráficos comparativos"""

    colors = ['#3498db', '#e74c3c', '#f39c12', '#27ae60', '#9b59b6', '#e67e22', '#1abc9c', '#34495e', '#16a085', '#f1c40f']

    # 1. Gráfico de evolução temporal - Top 5 dinâmico com linhas contínuas

    # Função para encontrar top 5 mais consistentes usando os dfs recebidos
    # (na visão global, esses dfs já representam o histórico completo)
    def get_top5_consistent_cryptos():
        crypto_appearances = {}

        for df_cur in dfs:
            if df_cur is None or df_cur.empty:
                continue
            if 'final_score' not in df_cur.columns:
                continue
            df_cur = df_cur.sort_values('final_score', ascending=False).reset_index(drop=True)
            top5 = df_cur.head(5)
            for _, row in top5.iterrows():
                symbol = row.get('symbol')
                if not symbol:
                    continue
                crypto_appearances[symbol] = crypto_appearances.get(symbol, 0) + 1

        return sorted(crypto_appearances.items(), key=lambda x: x[1], reverse=True)[:5]

    top5_cryptos = get_top5_consistent_cryptos()

    fig1 = go.Figure()

    # Para cada crypto no top 5 mais consistente, criar linha contínua
    for symbol, appearances in top5_cryptos:
        scores_timeline = []
        periods_timeline = []

        for i, df in enumerate(dfs):
            # Ordenar por score e calcular rank (não dependemos de coluna 'rank')
            df_sorted = df.sort_values('final_score', ascending=False).reset_index(drop=True)
            df_sorted['_rank'] = df_sorted.index + 1

            crypto_row = df_sorted[df_sorted['symbol'] == symbol]
            if not crypto_row.empty:
                rank_val = int(crypto_row.iloc[0]['_rank'])
                if rank_val <= 5:
                    scores_timeline.append(float(crypto_row.iloc[0]['final_score']))
                else:
                    scores_timeline.append(None)
            else:
                scores_timeline.append(None)

            periods_timeline.append(f'P{i+1}')

        # Adicionar trace com linha contínua (connectgaps=False para mostrar gaps)
        fig1.add_trace(go.Scatter(
            x=periods_timeline,
            y=scores_timeline,
            mode='lines+markers',
            name=f'{symbol} (Top5: {appearances}x)',
            line=dict(width=3),
            marker=dict(size=8),
            connectgaps=False  # Mostra gaps quando crypto sai do top 5
        ))

    fig1.update_layout(
        title='📈 EVOLUÇÃO TEMPORAL - TOP 5 MAIS CONSISTENTES (Histórico Completo)',
        xaxis_title='Períodos',
        yaxis_title='Score',
        height=500,
        template='plotly_white',
        hovermode='x unified'
    )

    # 2. Gráfico de consistência (lapidado: ordenado + aparições + cores diferenciadas)
    consistent_data = [item for item in crypto_ranking if item['consistency'] == 1.0]
    # Ordenar por score médio (maior para menor)
    consistent_data = sorted(consistent_data, key=lambda x: x['avg_score'], reverse=True)

    # Preparar cores e textos
    colors = []
    hover_texts = []
    for item in consistent_data:
        score = item['avg_score']
        # Cor diferenciada para score > 0.8
        if score > 0.8:
            colors.append('#27ae60')  # verde forte
        else:
            colors.append('#95a5a6')  # cinza
        # Texto com aparições (sempre total de períodos aqui)
        hover_texts.append(f"{item['symbol']}<br>Score Médio: {score:.3f}<br>Aparições: {len(dfs)}/{len(dfs)}")

    fig2 = go.Figure(data=[go.Bar(
        x=[item['symbol'] for item in consistent_data],
        y=[item['avg_score'] for item in consistent_data],
        marker_color=colors,
        text=[f'{item["avg_score"]:.3f}' for item in consistent_data],
        textposition='auto',
        hovertext=hover_texts,
        hoverinfo='text'
    )])

    fig2.update_layout(
        title='💎 CRYPTOS 100% CONSISTENTES (Presentes em todos períodos)',
        xaxis_title='Cryptomoedas',
        yaxis_title='Score Médio',
        height=400,
        template='plotly_white',
        xaxis={'categoryorder': 'array', 'categoryarray': [item['symbol'] for item in consistent_data]}
    )

    return "\n".join([
        "// Gráfico 1: Evolução Temporal",
        _fig_to_plotly_newplot_js(fig1, "top10-comparison-chart"),
        "// Gráfico 2: Consistência",
        _fig_to_plotly_newplot_js(fig2, "evolution-chart"),
    ])

def create_advanced_summary_table(top10, crypto_ranking, total_periods, historical_data=None, last_df=None):
    """Cria tabela de resumo avançado"""

    # Adicionar score_change ao crypto_ranking se disponível
    if last_df is not None and 'score_change' in last_df.columns:
        score_change_dict = dict(zip(last_df['symbol'], last_df['score_change']))
        for item in crypto_ranking:
            item['score_change'] = score_change_dict.get(item['symbol'], 0)

    # ===== TENDÊNCIAS (Δ Score) - Global e Recente =====
    # Usar global_dfs para deltas consistentes (primeiro vs último, e último vs 5 atrás)
    global_dfs = historical_data.get('global_dfs', [])
    if len(global_dfs) >= 2:
        # Delta Global: último - primeiro
        df_first = global_dfs[0]
        df_last = global_dfs[-1]
        delta_global_dict = {}
        if 'final_score' in df_first.columns and 'final_score' in df_last.columns:
            first_scores = dict(zip(df_first['symbol'], df_first['final_score']))
            last_scores = dict(zip(df_last['symbol'], df_last['final_score']))
            for symbol in set(first_scores) | set(last_scores):
                delta_global_dict[symbol] = last_scores.get(symbol, 0) - first_scores.get(symbol, 0)
        else:
            delta_global_dict = {}
        # Delta Recente (N=5): último - 5 atrás (ou primeiro se não tiver 5)
        recent_index = max(len(global_dfs) - 5, 0)
        df_recent_ref = global_dfs[recent_index]
        delta_recent_dict = {}
        if 'final_score' in df_recent_ref.columns and 'final_score' in df_last.columns:
            recent_ref_scores = dict(zip(df_recent_ref['symbol'], df_recent_ref['final_score']))
            for symbol in set(recent_ref_scores) | set(last_scores):
                delta_recent_dict[symbol] = last_scores.get(symbol, 0) - recent_ref_scores.get(symbol, 0)
        else:
            delta_recent_dict = {}
    else:
        delta_global_dict = {}
        delta_recent_dict = {}
        # Se não tiver global_dfs suficiente, fallback para last_df (se existir)
        if last_df is not None and 'score_change' in last_df.columns:
            delta_recent_dict = dict(zip(last_df['symbol'], last_df['score_change']))
            delta_global_dict = delta_recent_dict.copy()

    # Preparar deltas para cada crypto
    for item in crypto_ranking:
        item['delta_global'] = delta_global_dict.get(item['symbol'], 0)
        item['delta_recent'] = delta_recent_dict.get(item['symbol'], 0)

    # Ordenar para tendências
    top_growers_global = sorted([c for c in crypto_ranking if c['delta_global'] > 0], key=lambda x: x['delta_global'], reverse=True)[:5]
    top_fallers_global = sorted([c for c in crypto_ranking if c['delta_global'] < 0], key=lambda x: x['delta_global'])[:5]
    top_growers_recent = sorted([c for c in crypto_ranking if c['delta_recent'] > 0], key=lambda x: x['delta_recent'], reverse=True)[:5]
    top_fallers_recent = sorted([c for c in crypto_ranking if c['delta_recent'] < 0], key=lambda x: x['delta_recent'])[:5]

    # Renderizar HTML das duas seções
    def render_trend_block(title, growers, fallers, delta_key):
        growers_html = ''.join([
            f'<tr><td>{item["symbol"]}</td><td>+{item[delta_key]:.3f}</td></tr>'
            for item in growers
        ])
        fallers_html = ''.join([
            f'<tr><td>{item["symbol"]}</td><td>{item[delta_key]:.3f}</td></tr>'
            for item in fallers
        ])
        return f'''
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h4>{title}</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <h5>🚀 Maiores Crescimentos</h5>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="background-color: #27ae60; color: white;">
                            <th style="padding: 6px;">Crypto</th><th style="padding: 6px;">Δ Score</th>
                        </tr>
                        {growers_html if growers_html else '<tr><td colspan="2" style="text-align: center; color: #666;">Nenhum crescimento</td></tr>'}
                    </table>
                </div>
                <div>
                    <h5>⚠️ Maiores Quedas</h5>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="background-color: #e74c3c; color: white;">
                            <th style="padding: 6px;">Crypto</th><th style="padding: 6px;">Δ Score</th>
                        </tr>
                        {fallers_html if fallers_html else '<tr><td colspan="2" style="text-align: center; color: #666;">Nenhuma queda</td></tr>'}
                    </table>
                </div>
            </div>
        </div>
        '''

    trends_html = render_trend_block('📈 TENDÊNCIAS GLOBAIS (desde o 1º snapshot)', top_growers_global, top_fallers_global, 'delta_global')
    trends_html += render_trend_block('⚡ TENDÊNCIAS RECENTES (últimos 5 snapshots)', top_growers_recent, top_fallers_recent, 'delta_recent')

    # Estatísticas gerais
    total_unique = len(crypto_ranking)
    consistent_count = len([item for item in crypto_ranking if item['consistency'] == 1.0])
    new_count = len([item for item in crypto_ranking if item['presence_type'] == 'new'])
    gone_count = len([item for item in crypto_ranking if item['presence_type'] == 'gone'])

    return f"""
    <div class="stats">
        <!-- RESUMO GERAL -->
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h4>RESUMO GERAL</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                <div style="text-align: center; background-color: white; padding: 10px; border-radius: 5px;">
                    <strong>{total_unique}</strong><br>
                    <small>Total Cryptos</small>
                </div>
                <div style="text-align: center; background-color: white; padding: 10px; border-radius: 5px;">
                    <strong>{((new_count + gone_count) / total_unique * 100):.1f}%</strong><br>
                    <small>Rotatividade</small>
                </div>
                <div style="text-align: center; background-color: white; padding: 10px; border-radius: 5px;">
                    <strong>{sum(item["avg_score"] for item in crypto_ranking) / total_unique:.3f}</strong><br>
                    <small>Score Médio Geral</small>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
                <div style="text-align: center; background-color: white; padding: 10px; border-radius: 5px;">
                    <strong>{consistent_count}</strong><br>
                    <small>100% Consistentes</small>
                </div>
                <div style="text-align: center; background-color: white; padding: 10px; border-radius: 5px;">
                    <strong>{new_count}</strong><br>
                    <small> Novas</small>
                </div>
                <div style="text-align: center; background-color: white; padding: 10px; border-radius: 5px;">
                    <strong>{gone_count}</strong><br>
                    <small> Saíram</small>
                </div>
            </div>
        </div>

        <!-- TOP PERFORMERS -->
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h4>TOP PERFORMERS (Melhores Scores)</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #27ae60; color: white;">
                    <th style="padding: 8px; text-align: left;">Crypto</th>
                    <th style="padding: 8px; text-align: center;">Score Médio</th>
                    <th style="padding: 8px; text-align: center;">Consistência</th>
                    <th style="padding: 8px; text-align: center;">Performance</th>
                </tr>
                {''.join([f'''
                <tr>
                    <td style="padding: 8px;"><strong>{item["symbol"]}</strong></td>
                    <td style="padding: 8px; text-align: center;">{item["avg_score"]:.3f}</td>
                    <td style="padding: 8px; text-align: center;">{item["consistency"]*100:.0f}%</td>
                    <td style="padding: 8px; text-align: center;">
                        {"🔥" if item["avg_score"] > 0.8 else "⭐" if item["avg_score"] > 0.6 else "📊"}
                    </td>
                </tr>
                ''' for item in sorted(crypto_ranking, key=lambda x: x["avg_score"], reverse=True)[:5]])}
            </table>
        </div>

        {trends_html}
    </div>
    """

def create_presence_heatmap(crypto_ranking, snapshot_info):
    """Cria heatmap de presença de cryptos"""

    # Preparar dados para heatmap
    symbols = [item['symbol'] for item in crypto_ranking]
    periods = [f'P{i+1}' for i in range(len(snapshot_info))]

    heatmap_data = []
    for item in crypto_ranking:
        row = []
        for i in range(len(snapshot_info)):
            if i in item['periods_present']:
                # Score presente
                score_idx = item['periods_present'].index(i)
                score = item['scores'][score_idx]
                row.append(score)
            else:
                row.append(0)
        heatmap_data.append(row)

    return f"""
    <div class="stats">
        <h4>🔥 HEATMAP DE PRESENÇA E SCORE</h4>
        <p style="font-size: 12px; color: #666;">Quanto mais intenso, maior o score. Branco = ausente.</p>

        <div style="display: grid; grid-template-columns: auto repeat({len(snapshot_info)}, 1fr); gap: 2px; font-size: 11px;">
            <div></div>
            {''.join([f'<div style="text-align: center; font-weight: bold;">{period}</div>' for period in periods])}

            {''.join([
                f'''
                <div style="text-align: right; padding-right: 5px; font-weight: bold;">{symbol}</div>
                ''' + ''.join([
                    f'''
                    <div style="
                        background-color: {"rgba(46, 204, 113, " + str(min(score, 1.0)) + ")" if score > 0 else "white"};
                        border: 1px solid #ddd;
                        text-align: center;
                        padding: 2px;
                        color: {"white" if score > 0.5 else "black"};
                        font-weight: bold;
                    ">
                        {f"{score:.2f}" if score > 0 else ""}
                    </div>
                    ''' for score in row
                ])
                for symbol, row in zip(symbols, heatmap_data)
            ])}
        </div>

        <div style="margin-top: 10px; font-size: 12px;">
            <span style="display: inline-block; width: 20px; height: 20px; background: rgba(46, 204, 113, 0.2); border: 1px solid #ddd;"></span> Baixo Score
            <span style="display: inline-block; width: 20px; height: 20px; background: rgba(46, 204, 113, 0.8); border: 1px solid #ddd; margin-left: 10px;"></span> Alto Score
            <span style="display: inline-block; width: 20px; height: 20px; background: white; border: 1px solid #ddd; margin-left: 10px;"></span> Ausente
        </div>
    </div>
    """

def create_period_html(df, snapshot_info, index):
    """Cria HTML para um período específico"""

    # Preparar dados para o período
    display_cols = ['symbol', 'name', 'market_cap', 'total_volume', 'price_change_percentage_24h']

    if 'ratio' in df.columns:
        display_cols.append('ratio')
    if 'final_score' in df.columns:
        display_cols.append('final_score')

    if 'persistence_count_3d' in df.columns:
        display_cols.extend(['persistence_count_3d', 'persistence_count_7d', 'persistence_count_14d'])

    if 'timeframe_classification' in df.columns:
        display_cols.extend(['timeframe_classification'])
    if 'is_confirmed_leader' in df.columns:
        display_cols.extend(['is_confirmed_leader'])

    if 'zone' in df.columns:
        display_cols.extend(['zone'])
    if 'momentum' in df.columns:
        display_cols.extend(['momentum'])
    if 'is_gold' in df.columns:
        display_cols.extend(['is_gold'])
    if 'rs_strong' in df.columns:
        display_cols.extend(['rs_strong'])

    # Filtrar colunas existentes
    table_df = df[[col for col in display_cols if col in df.columns]].copy()

    # Ordenar por final_score ou ratio
    if 'final_score' in table_df.columns:
        table_df = table_df.sort_values('final_score', ascending=False)
    elif 'ratio' in table_df.columns:
        table_df = table_df.sort_values('ratio', ascending=False)

    # Formatar colunas
    table_df['market_cap'] = table_df['market_cap'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else 'N/A')
    table_df['total_volume'] = table_df['total_volume'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else 'N/A')
    table_df['price_change_percentage_24h'] = table_df['price_change_percentage_24h'].apply(
        lambda x: f"{x:.1f}%" if pd.notna(x) else 'N/A'
    )

    if 'ratio' in table_df.columns:
        table_df['ratio'] = table_df['ratio'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')

    if 'final_score' in table_df.columns:
        table_df['final_score'] = table_df['final_score'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')

    # Formatar contadores de persistência
    if 'persistence_count_3d' in table_df.columns:
        table_df['persistence_count_3d'] = table_df['persistence_count_3d'].apply(lambda x: f"{x}x")
        table_df['persistence_count_7d'] = table_df['persistence_count_7d'].apply(lambda x: f"{x}x")
        table_df['persistence_count_14d'] = table_df['persistence_count_14d'].apply(lambda x: f"{x}x")

    # Formatar colunas de liderança
    if 'timeframe_classification' in table_df.columns:
        table_df['timeframe_classification'] = table_df['timeframe_classification'].apply(
            lambda x: x.replace('_', ' ').title() if pd.notna(x) else 'Unknown'
        )
    if 'is_confirmed_leader' in table_df.columns:
        table_df['is_confirmed_leader'] = table_df['is_confirmed_leader'].apply(
            lambda x: '👑 YES' if x else '❌ NO'
        )

    # Formatar colunas de análise técnica
    if 'zone' in table_df.columns:
        table_df['zone'] = table_df['zone'].apply(
            lambda x: (
                f"🔥 {x.replace('_', ' ').title()}" if x == 'breakout' else
                f"🟠 {x.replace('_', ' ').title()}" if x == 'strong' else
                f"🟡 {x.replace('_', ' ').title()}" if x == 'early_accumulation' else
                f"⚪ {x.replace('_', ' ').title()}"
            ) if pd.notna(x) else 'Unknown'
        )
    if 'momentum' in table_df.columns:
        table_df['momentum'] = table_df['momentum'].apply(
            lambda x: f"{'🔥 High' if x == 'high' else '📈 Medium' if x == 'medium' else '📊 Low'}" if pd.notna(x) else 'Unknown'
        )
    if 'is_gold' in table_df.columns:
        table_df['is_gold'] = table_df['is_gold'].apply(
            lambda x: '👑 Gold' if x else '⚪ Normal'
        )
    if 'rs_strong' in table_df.columns:
        table_df['rs_strong'] = table_df['rs_strong'].apply(
            lambda x: '💪 Strong' if x else '⚪ Normal'
        )

    # Renomear colunas
    column_mapping = {
        'symbol': 'Symbol',
        'name': 'Name',
        'market_cap': 'Market Cap',
        'total_volume': 'Volume',
        'price_change_percentage_24h': '24h%',
        'ratio': 'Ratio',
        'final_score': 'Score',
        'persistence_count_3d': '3d',
        'persistence_count_7d': '7d',
        'persistence_count_14d': '14d',
        'timeframe_classification': 'Classification',
        'is_confirmed_leader': 'Leader',
        'zone': 'Zone',
        'momentum': 'Momentum',
        'is_gold': 'Gold',
        'rs_strong': 'RS'
    }

    table_df.rename(columns=column_mapping, inplace=True)

    # Criar tabela HTML
    table_html = table_df.to_html(classes='table table-striped', index=False)

    # Estatísticas do período
    mc_mean = df['market_cap'].mean()
    volume_total = df['total_volume'].sum()
    positive_changes = (df['price_change_percentage_24h'] > 0).sum()

    period_html = f"""
    <div class="stats">
        <h3>📊 Estatísticas - {snapshot_info["date"]}</h3>
        <p><strong>Market Cap Médio:</strong> ${mc_mean:,.0f}</p>
        <p><strong>Volume Total:</strong> ${volume_total:,.0f}</p>
        <p><strong>Variação 24h Positivas:</strong> {positive_changes}/{len(df)} ({positive_changes/len(df)*100:.1f}%)</p>
    </div>

    <h3>📋 Dados Completos - {snapshot_info["date"]}</h3>
    {table_html}
    """

    return period_html

def show_latest_csv(specific_file=None):
    """Mostra CSV com visualização Plotly (mais recente ou específico)"""

    if specific_file:
        print(f"🔍 CARREGANDO SNAPSHOT ESPECÍFICO...")
        file_path = specific_file
        latest_file = os.path.basename(file_path)
    else:
        print("🔍 BUSCANDO CSV MAIS RECENTE...")
        snapshots_dir = "data/snapshots"
        if not os.path.exists(snapshots_dir):
            print("❌ Pasta snapshots não encontrada")
            return

        # Encontrar enhanced CSV mais recente
        csv_files = [f for f in os.listdir(snapshots_dir)
                     if f.endswith('.csv') and 'enhanced_' in f]
        if not csv_files:
            print("❌ Nenhum CSV enhanced encontrado")
            return

        csv_files.sort(reverse=True)
        latest_file = csv_files[0]
        file_path = os.path.join(snapshots_dir, latest_file)

    print(f"📁 Arquivo: {latest_file}")
    print(f"📅 Modificado: {datetime.fromtimestamp(os.path.getmtime(file_path))}")
    print()

    try:
        df = pd.read_csv(file_path)
        print(f"📊 Dados: {len(df)} gems, {len(df.columns)} colunas")
        print()

        # 📊 Estatísticas rápidas
        mcs = df['market_cap']
        volumes = df['total_volume'].fillna(0)
        changes = df['price_change_percentage_24h'].fillna(0)

        print("📊 ESTATÍSTICAS RÁPIDAS:")
        print("-" * 40)
        print(f"Market Cap - Médio: ${mcs.mean():,.0f}")
        print(f"Market Cap - Min/Max: ${mcs.min():,} / ${mcs.max():,}")
        print(f"Volume Total - Total: ${volumes.sum():,.0f}")
        print(f"Variação 24h - Positivas: {(changes > 0).sum()}/{len(changes)} ({(changes > 0).mean()*100:.1f}%)")
        print()

        # 🏆 Eventos especiais (se tiver enhanced)
        if 'is_confirmed_leader' in df.columns:
            print("🏆 EVENTOS ESPECIAIS:")
            print("-" * 30)
            leaders = df['is_confirmed_leader'].sum()
            social = df['social_explosion'].sum() if 'social_explosion' in df.columns else 0
            rs_strong = df['rs_strong'].sum() if 'rs_strong' in df.columns else 0

            print(f"👑 Líderes confirmados: {leaders}")
            print(f"🔥 Explosões sociais: {social}")
            print(f"💪 RS vs BTC forte: {rs_strong}")
            print()

        # 🎨 Criar visualização interativa
        print("🎨 CRIANDO VISUALIZAÇÃO INTERATIVA...")

        # Dashboard principal
        create_interactive_dashboard(df, latest_file)

    except Exception as e:
        print(f"❌ Erro ao processar CSV: {e}")
        return None

def main():
    print("📊 GEMS SYSTEM - VISUALIZADOR INTERATIVO (PLOTLY)")
    print("=" * 60)
    print()

    while True:
        print("Escolha uma opção:")
        print("1. ⭐ Comparar snapshots (DASHBOARD AVANÇADO)")
        print("2. � Ver snapshot mais recente")
        print("3. � Escolher snapshot específico")
        print("4. 📁 Listar todos os CSVs")
        print("0. 🚪 Sair")
        print()

        choice = input("Opção (0-4) [ENTER = 1]: ").strip()

        if choice == '' or choice == '1':
            show_comparison_snapshots()
            print()
        elif choice == '2':
            show_latest_csv()
            print()
        elif choice == '3':
            selected_file = show_snapshot_selection()
            if selected_file:
                file_path = os.path.join("data/snapshots", selected_file)
                show_latest_csv(file_path)
            print()
        elif choice == '4':
            # Listar CSVs
            csv_files = get_available_snapshots()
            if csv_files:
                print("📁 CSVs disponíveis:")
                for i, file in enumerate(csv_files[:15], 1):
                    print(f"{i:2d}. {file}")
                print(f"Total: {len(csv_files)} arquivos")
            else:
                print("❌ Nenhum snapshot encontrado")
            print()
        elif choice == '0':
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida")
            print()

if __name__ == "__main__":
    main()
