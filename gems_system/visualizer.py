#!/usr/bin/env python3
"""
📊 Visualizador interativo com Plotly + Pandas
Abre gráficos interativos no navegador - sem servidor!
"""
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime
import webbrowser
import tempfile

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

    # 1. Market Cap Top 15
    top15_mc = df.nlargest(15, 'market_cap').sort_values('market_cap')
    fig.add_trace(
        go.Bar(
            y=top15_mc['symbol'],
            x=top15_mc['market_cap']/1e6,
            orientation='h',
            name='Market Cap',
            marker_color='lightblue',
            hovertemplate='<b>%{y}</b><br>MC: $%{x:,.0f}M<extra></extra>'
        ),
        row=1, col=1
    )

    # 2. Ratio Top 15
    top15_ratio = df.nlargest(15, 'ratio').sort_values('ratio')
    fig.add_trace(
        go.Bar(
            y=top15_ratio['symbol'],
            x=top15_ratio['ratio'],
            orientation='h',
            name='Volume/MC Ratio',
            marker_color='lightgreen',
            hovertemplate='<b>%{y}</b><br>Ratio: %{x:.3f}<extra></extra>'
        ),
        row=1, col=2
    )

    # 3. Variação 24h
    top15_change = df.nlargest(15, 'price_change_percentage_24h').sort_values('price_change_percentage_24h')
    colors = ['green' if x >= 0 else 'red' for x in top15_change['price_change_percentage_24h']]
    fig.add_trace(
        go.Bar(
            y=top15_change['symbol'],
            x=top15_change['price_change_percentage_24h'],
            orientation='h',
            name='Variação 24h',
            marker_color=colors,
            hovertemplate='<b>%{y}</b><br>24h: %{x:+.2f}%<extra></extra>'
        ),
        row=2, col=1
    )

    # 4. Final Score (se tiver)
    if 'final_score' in df.columns:
        top15_score = df.nlargest(15, 'final_score').sort_values('final_score')
        fig.add_trace(
            go.Bar(
                y=top15_score['symbol'],
                x=top15_score['final_score'],
                orientation='h',
                name='Final Score',
                marker_color='orange',
                hovertemplate='<b>%{y}</b><br>Score: %{x:.2f}<extra></extra>'
            ),
            row=2, col=2
        )
    else:
        # Se não tiver score, mostrar volume
        top15_vol = df.nlargest(15, 'total_volume').sort_values('total_volume')
        fig.add_trace(
            go.Bar(
                y=top15_vol['symbol'],
                x=top15_vol['total_volume']/1e6,
                orientation='h',
                name='Volume Total',
                marker_color='orange',
                hovertemplate='<b>%{y}</b><br>Vol: $%{x:,.0f}M<extra></extra>'
            ),
            row=2, col=2
        )

    # Layout
    fig.update_layout(
        title_text=f"🚀 GEMS SYSTEM DASHBOARD - {file_name}",
        title_x=0.5,
        height=800,
        showlegend=False,
        template='plotly_white'
    )

    # Eixos
    fig.update_xaxes(title_text="Market Cap (M USD)", row=1, col=1)
    fig.update_xaxes(title_text="Volume/MC Ratio", row=1, col=2)
    fig.update_xaxes(title_text="Variação 24h (%)", row=2, col=1)
    fig.update_xaxes(title_text="Final Score" if 'final_score' in df.columns else "Volume (M USD)", row=2, col=2)

    return fig

def create_data_table(df):
    """Cria tabela interativa com dados principais"""

    # Preparar dados para tabela
    display_cols = ['symbol', 'name', 'market_cap', 'total_volume', 'price_change_percentage_24h']
    if 'final_score' in df.columns:
        display_cols.extend(['ratio', 'final_score'])

    # Adicionar colunas de persistência se existirem (apenas contadores)
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

    table_df = df[display_cols].copy()

    # Formatar colunas
    table_df['market_cap'] = table_df['market_cap'].apply(lambda x: f"${x:,.0f}")
    table_df['total_volume'] = table_df['total_volume'].fillna(0).apply(lambda x: f"${x:,.0f}")
    table_df['price_change_percentage_24h'] = table_df['price_change_percentage_24h'].fillna(0).apply(lambda x: f"{x:+.2f}%")

    if 'ratio' in table_df.columns:
        table_df['ratio'] = table_df['ratio'].apply(lambda x: f"{x:.3f}")
    if 'final_score' in table_df.columns:
        table_df['final_score'] = table_df['final_score'].apply(lambda x: f"{x:.2f}")

    # Formatar colunas de persistência (apenas contadores)
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

    # Renomear colunas base
    base_cols = ['Symbol', 'Name', 'Market Cap', 'Volume', '24h%']
    if 'final_score' in df.columns:
        base_cols.extend(['Ratio', 'Score'])

    # Adicionar colunas de persistência (apenas contadores)
    if 'persistence_count_3d' in df.columns:
        base_cols.extend(['3d', '7d', '14d'])

    # Adicionar colunas de liderança
    if 'timeframe_classification' in df.columns:
        base_cols.extend(['Classification'])
    if 'is_confirmed_leader' in df.columns:
        base_cols.extend(['Leader'])

    # Adicionar colunas de análise técnica
    if 'zone' in df.columns:
        base_cols.extend(['Zone'])
    if 'momentum' in df.columns:
        base_cols.extend(['Momentum'])
    if 'is_gold' in df.columns:
        base_cols.extend(['Gold'])
    if 'rs_strong' in df.columns:
        base_cols.extend(['RS'])

    table_df.columns = base_cols

    # Criar figura com tabela
    fig_table = go.Figure(data=[go.Table(
        header=dict(
            values=list(table_df.columns),
            fill_color='lightblue',
            align='left',
            font=dict(size=12, color='black')
        ),
        cells=dict(
            values=[table_df[col] for col in table_df.columns],
            fill_color='white',
            align='left',
            font=dict(size=10, color='black')
        )
    )])

    fig_table.update_layout(
        title="📊 DADOS COMPLETOS",
        title_x=0.5,
        height=600,
        template='plotly_white'
    )

    return fig_table

def show_latest_csv():
    """Mostra CSV mais recente com visualização Plotly"""
    print("🔍 BUSCANDO CSV MAIS RECENTE...")

    snapshots_dir = "data/snapshots"
    if not os.path.exists(snapshots_dir):
        print("❌ Pasta snapshots não encontrada")
        return

    # Encontrar CSV mais recente
    csv_files = [f for f in os.listdir(snapshots_dir) if f.endswith('.csv')]
    if not csv_files:
        print("❌ Nenhum CSV encontrado")
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

        # 📊 Estatísticas rápidas no terminal
        print("📊 ESTATÍSTICAS RÁPIDAS:")
        print("-" * 40)
        mcs = df['market_cap']
        volumes = df['total_volume'].fillna(0)
        changes = df['price_change_percentage_24h'].fillna(0)

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

        # 🎯 Criar visualização interativa
        print("🎨 CRIANDO VISUALIZAÇÃO INTERATIVA...")

        # Dashboard principal
        fig_dashboard = create_interactive_dashboard(df, latest_file)

        # Tabela de dados
        fig_table = create_data_table(df)

        # Criar HTML temporário e abrir diretamente
        import tempfile

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
                <p><strong>Arquivo:</strong> {latest_file}</p>
                <p><strong>Data:</strong> {datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Gems:</strong> {len(df)} | <strong>Colunas:</strong> {len(df.columns)}</p>

                <div class="stats">
                    <h3>📊 Estatísticas</h3>
                    <p><strong>Market Cap Médio:</strong> ${mcs.mean():,.0f}</p>
                    <p><strong>Volume Total:</strong> ${volumes.sum():,.0f}</p>
                    <p><strong>Variação 24h Positivas:</strong> {(changes > 0).sum()}/{len(changes)} ({(changes > 0).mean()*100:.1f}%)</p>
                </div>

                {f'<div class="stats"><h3>🏆 Eventos Especiais</h3><span class="event leader">👑 Líderes: {leaders}</span><span class="event social">🔥 Sociais: {social}</span><span class="event rs">💪 RS: {rs_strong}</span></div>' if 'is_confirmed_leader' in df.columns else ''}

                <div id="dashboard"></div>

                <div id="table" style="margin-top: 30px;"></div>
            </div>

            <script>
                {fig_dashboard.to_html(div_id="dashboard", include_plotlyjs=False)}
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

    except Exception as e:
        print(f"❌ Erro ao processar CSV: {e}")
        return None

def main():
    print("📊 GEMS SYSTEM - VISUALIZADOR INTERATIVO (PLOTLY)")
    print("=" * 60)
    print()

    while True:
        print("Escolha uma opção:")
        print("1. 📊 Ver CSV mais recente (dashboard interativo)")
        print("2. 📁 Listar todos os CSVs")
        print("3. 🚪 Sair")
        print()

        choice = input("Opção (1-3): ").strip()

        if choice == '1':
            show_latest_csv()
            print()
        elif choice == '2':
            # Listar CSVs
            snapshots_dir = "data/snapshots"
            if os.path.exists(snapshots_dir):
                csv_files = [f for f in os.listdir(snapshots_dir) if f.endswith('.csv')]
                csv_files.sort(reverse=True)
                print("📁 CSVs disponíveis:")
                for i, file in enumerate(csv_files[:10], 1):
                    print(f"{i:2d}. {file}")
                print()
            else:
                print("❌ Pasta snapshots não encontrada")
                print()
        elif choice == '3':
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida")
            print()

if __name__ == "__main__":
    main()
