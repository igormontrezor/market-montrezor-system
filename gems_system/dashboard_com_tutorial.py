"""
GEMS DASHBOARD COM TUTORIAIS
Dashboard interativo com tutoriais explicativos para cada gráfico
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime
import webbrowser
import os

# Importar funções existentes
from visualizer import (
    load_all_snapshots,
    create_all_comparison_charts,
    create_hall_of_fame,
    create_global_evolution_block
)

def create_ranking_header():
    """HTML com ranking dos gráficos por importância"""
    return """
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; margin-bottom: 30px; color: white;">
        <h1 style="text-align: center; margin-bottom: 30px;">🎯 GEMS SYSTEM - GUIA COMPLETO DE ANÁLISE</h1>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3>🥇 1º - BUBBLE CHART</h3>
                <p><strong>O mais importante para encontrar oportunidades!</strong></p>
                <p>Identifica micro caps com explosão de volume (potencial 10x-100x).</p>
            </div>

            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3>🥈 2º - ACUMULAÇÃO SILENCIOSA</h3>
                <p><strong>Detecta dinheiro inteligente entrando!</strong></p>
                <p>Mostra acumulação gradual antes dos pumps.</p>
            </div>

            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3>🥉 3º - HEATMAP SETORIAL</h3>
                <p><strong>Para onde o dinheiro está fluindo?</strong></p>
                <p>Identifica setores em alta vs baixa.</p>
            </div>

            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3>4º - EVOLUÇÃO TEMPORAL</h3>
                <p><strong>Acompanha o progresso das gems.</strong></p>
                <p>Mostra evolução do ratio ao longo do tempo.</p>
            </div>

            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3>5º - CONSISTÊNCIA</h3>
                <p><strong>Separando líderes de spikes.</strong></p>
                <p>Quantos dias cada gem se manteve forte.</p>
            </div>

            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3>6º - PERSISTÊNCIA</h3>
                <p><strong>Mapa de calor histórico.</strong></p>
                <p>Visualização rápida de padrões.</p>
            </div>
        </div>

        <div style="text-align: center; margin-top: 20px;">
            <p style="font-size: 18px;"><strong>💡 Dica:</strong> Comece pelo Bubble Chart, depois verifique a Acumulação Silenciosa!</p>
        </div>
    </div>
    """

def create_strategy_section():
    """HTML com estratégias de uso dos gráficos"""
    return """
    <div style="background-color: #f8f9fa; padding: 30px; border-radius: 15px; margin-bottom: 30px;">
        <h2 style="color: #2c3e50; text-align: center; margin-bottom: 30px;">🎯 ESTRATÉGIAS DE ANÁLISE</h2>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 25px;">
            <div style="background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #e74c3c;">🚀 Estratégia RÁPIDA (Scalping)</h3>
                <ol style="line-height: 1.8;">
                    <li><strong>Bubble Chart:</strong> Bolhas pequenas no topo (MC baixo + Ratio alto)</li>
                    <li><strong>Acumulação:</strong> Picos recentes no gráfico de acumulação</li>
                    <li><strong>Setor:</strong> Setor verde no heatmap (dinheiro entrando)</li>
                    <li><strong>Meta:</strong> Entrar rápido, sair em 2-5 dias</li>
                </ol>
            </div>

            <div style="background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #27ae60;">📈 Estratégia MÉDIA (Swing)</h3>
                <ol style="line-height: 1.8;">
                    <li><strong>Bubble Chart:</strong> Bolhas médias-altas com ratio consistente</li>
                    <li><strong>Consistência:</strong> 5-10 dias no gráfico de barras</li>
                    <li><strong>Acumulação:</strong> Tendência de alta suave</li>
                    <li><strong>Meta:</strong> Segurar 1-3 semanas</li>
                </ol>
            </div>

            <div style="background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #3498db;">👑 Estratégia LONGA (Position)</h3>
                <ol style="line-height: 1.8;">
                    <li><strong>Consistência:</strong> 15+ dias persistência</li>
                    <li><strong>Heatmap:</strong> Linhas verdes contínuas</li>
                    <li><strong>Evolução:</strong> Tendência de alta estável</li>
                    <li><strong>Meta:</strong> Segurar 1-3 meses</li>
                </ol>
            </div>
        </div>

        <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin-top: 25px; border-left: 5px solid #ffc107;">
            <h4 style="color: #856404; margin-top: 0;">⚠️ GESTÃO DE RISCO</h4>
            <ul style="margin-bottom: 0;">
                <li><strong>Nunca invista mais de 5% em uma única gem</strong></li>
                <li><strong>Diversifique entre 3-5 gems diferentes</strong></li>
                <li><strong>Use stop-loss de 15-20%</strong></li>
                <li><strong>Tome lucro parcial em 2x, 3x, 5x</strong></li>
            </ul>
        </div>
    </div>
    """

def create_complete_dashboard():
    """Dashboard completo com tutoriais e estratégias"""

    # Carregar dados
    print("📊 Carregando snapshots...")
    historical_data = load_all_snapshots()

    if not historical_data:
        print("❌ Nenhum snapshot encontrado!")
        return

    # Pegar snapshots mais recentes
    recent_snapshots = sorted(historical_data.keys(), reverse=True)[:2]
    dfs = {date: historical_data[date] for date in recent_snapshots}

    # Criar gráficos
    print("🎨 Criando gráficos...")
    js_block = create_all_comparison_charts(recent_snapshots[-1], dfs)

    # Criar resumos
    summary_html = ""
    hall_html = create_hall_of_fame(historical_data, recent_snapshots[-1])

    # HTML completo
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GEMS SYSTEM - Dashboard Completo com Tutoriais</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f6fa; }}
            .container {{ max-width: 1400px; margin: 0 auto; }}
            h1, h2, h3 {{ color: #2c3e50; }}
        </style>
    </head>
    <body>
        <div class="container">
            {create_ranking_header()}
            {create_strategy_section()}

            <!-- Gráficos com tutoriais -->
            <div style="background-color: #ecf0f1; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
                <h3 style="text-align: center; color: #2c3e50;">📈 ANÁLISE COMPLETA DOS GRÁFICOS</h3>

                <!-- Gráfico 1: Evolução Temporal -->
                <div id="top10-comparison-chart"></div>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #3498db;">
                    <h4 style="margin-top: 0; color: #2c3e50;">📊 <strong>Tutorial - Gráfico de Evolução Temporal</strong></h4>
                    <p style="margin-bottom: 10px;"><strong>O que mostra:</strong> A evolução do Ratio Volume/MC das top 10 gems ao longo do tempo.</p>
                    <p style="margin-bottom: 10px;"><strong>Como interpretar:</strong></p>
                    <ul style="margin-left: 20px; margin-bottom: 10px;">
                        <li><strong>Linhas subindo:</strong> Gems ganhando interesse e volume real</li>
                        <li><strong>Linhas estáveis altas:</strong> Gems consolidadas com liquidez constante</li>
                        <li><strong>Linhas caindo:</strong> Gems perdendo interesse/volume</li>
                    </ul>
                    <p style="margin-bottom: 0;"><strong>Exemplo prático:</strong> Se você vir uma linha passando de 0.3 para 1.2 em poucos dias, essa gem está tendo uma explosão de volume - ótima oportunidade!</p>
                </div>

                <!-- Gráfico 2: Consistência -->
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

                <!-- Gráfico 3: Bubble Chart (O MAIS IMPORTANTE) -->
                <div id="bubble-chart" style="margin-top: 30px;"></div>
                <div style="background-color: #ffeaa7; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #e74c3c;">
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
                    <p style="margin-bottom: 0;"><strong>Exemplo prático:</strong> Bolha pequena no topo = micro cap com explosão de volume = potencial 10x-100x!</p>
                </div>

                <!-- Gráfico 4: Heatmap de Persistência -->
                <div id="persistence-heatmap" style="margin-top: 30px;"></div>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #f39c12;">
                    <h4 style="margin-top: 0; color: #2c3e50;">🔥 <strong>Tutorial - Heatmap de Persistência</strong></h4>
                    <p style="margin-bottom: 10px;"><strong>O que mostra:</strong> Quais gems foram consistentes em cada snapshot.</p>
                    <p style="margin-bottom: 10px;"><strong>Como interpretar:</strong></p>
                    <ul style="margin-left: 20px; margin-bottom: 10px;">
                        <li><strong>Verdes escuros:</strong> Gems sempre fortes (líderes confirmados)</li>
                        <li><strong>Amarelos:</strong> Gems intermitentes (potenciais)</li>
                        <li><strong>Vermelhos:</strong> Gems fracassadas ou spikes</li>
                    </ul>
                    <p style="margin-bottom: 0;"><strong>Exemplo prático:</strong> Uma linha verde horizontal contínua indica uma gem que nunca decepcionou - excelente para longo prazo!</p>
                </div>

                <!-- Gráfico 5: Acumulação Silenciosa -->
                <div id="accumulation-chart" style="margin-top: 30px;"></div>
                <div style="background-color: #d1f2eb; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #27ae60;">
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

                <!-- Gráfico 6: Heatmap Setorial -->
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
                    <p style="margin-bottom: 0;"><strong>Exemplo prático:</strong> Se "DeFi" está vermelho escuro e "Gaming" branco, o dinheiro está saindo de Gaming para DeFi - compre Gaming (frio) ou siga DeFi (quente)!</p>
                </div>

                <div id="ranking-summary" style="margin-top: 20px;"></div>
                <div id="hall-of-fame" style="margin-top: 20px;"></div>
            </div>
        </div>

        <script>
            {js_block}
            document.getElementById('ranking-summary').innerHTML = `{summary_html.replace('`', chr(96))}`;
            document.getElementById('hall-of-fame').innerHTML = `{hall_html.replace('`', chr(96))}`;
        </script>
    </body>
    </html>
    """

    # Salvar arquivo
    output_file = "dashboard_completo_com_tutorial.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Dashboard salvo: {output_file}")
    print("🌐 Abrindo no navegador...")

    # Abrir no navegador
    webbrowser.open(f'file://{os.path.abspath(output_file)}')

    return output_file

if __name__ == "__main__":
    create_complete_dashboard()
