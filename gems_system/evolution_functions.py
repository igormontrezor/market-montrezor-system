"""
🚀 Funções para Análise Evolutiva de Cryptos - Módulo Complementar
Implementa Opção 4 + Opção 3: Dashboard Evolutivo Completo com Timeline
"""
import os
import pandas as pd
from datetime import datetime, timedelta

def get_all_snapshots_for_evolution():
    """Coleta TODOS os snapshots disponíveis para análise evolutiva completa"""
    snapshots_dir = "data/snapshots"
    if not os.path.exists(snapshots_dir):
        return []

    # Encontrar todos os enhanced CSVs
    csv_files = [f for f in os.listdir(snapshots_dir)
                 if f.endswith('.csv') and 'enhanced_' in f]
    csv_files.sort()  # Ordem cronológica

    all_snapshots = []
    for file in csv_files:
        file_path = os.path.join(snapshots_dir, file)
        try:
            df = pd.read_csv(file_path)

            # Extrair data/hora do arquivo
            date_part = file.split('enhanced_')[1].replace('.csv', '')
            date_str = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]} {date_part[9:11]}:{date_part[11:13]}"

            all_snapshots.append({
                'file': file,
                'date': date_str,
                'df': df,
                'count': len(df)
            })
        except Exception as e:
            print(f"⚠️ Erro ao carregar {file}: {e}")

    return all_snapshots

def analyze_historical_evolution(all_snapshots_data, current_dfs):
    """Analisa evolução histórica completa de todas as cryptos"""

    # Coletar universo de cryptos que já estiveram no TOP
    historical_top10 = set()
    snapshot_timeline = []

    for snapshot in all_snapshots_data:
        df = snapshot['df']
        date = snapshot['date']

        # Ordenar por score ou ratio
        if 'final_score' in df.columns:
            sorted_df = df.sort_values('final_score', ascending=False)
        elif 'ratio' in df.columns:
            sorted_df = df.sort_values('ratio', ascending=False)
        else:
            sorted_df = df.sort_values('market_cap', ascending=False)

        # Pegar TOP 10
        top10 = sorted_df.head(10)

        snapshot_data = {
            'date': date,
            'top10_symbols': top10['symbol'].tolist(),
            'top10_scores': top10['final_score'].tolist() if 'final_score' in top10.columns else top10['ratio'].tolist()
        }

        snapshot_timeline.append(snapshot_data)
        historical_top10.update(top10['symbol'].tolist())

    # Criar timeline para cada crypto
    crypto_timeline = {}
    for crypto in historical_top10:
        timeline_data = {
            'symbol': crypto,
            'positions': [],
            'scores': [],
            'dates': [],
            'status': [],  # 'active', 'fallen', 'recovered'
            'consecutive_days': 0,
            'max_consecutive': 0,
            'total_appearances': 0,
            'avg_position': 0,
            'best_position': 999,
            'current_streak': 0,
            'last_seen': None
        }

        # Analisar cada snapshot
        for snapshot in snapshot_timeline:
            if crypto in snapshot['top10_symbols']:
                position = snapshot['top10_symbols'].index(crypto) + 1
                score = snapshot['top10_scores'][snapshot['top10_symbols'].index(crypto)]

                timeline_data['positions'].append(position)
                timeline_data['scores'].append(score)
                timeline_data['dates'].append(snapshot['date'])
                timeline_data['status'].append('active')
                timeline_data['total_appearances'] += 1
                timeline_data['current_streak'] += 1
                timeline_data['last_seen'] = snapshot['date']

                if position < timeline_data['best_position']:
                    timeline_data['best_position'] = position

                if timeline_data['current_streak'] > timeline_data['max_consecutive']:
                    timeline_data['max_consecutive'] = timeline_data['current_streak']
            else:
                # Crypto não está no TOP 10 deste período
                timeline_data['positions'].append(None)
                timeline_data['scores'].append(0)
                timeline_data['dates'].append(snapshot['date'])
                timeline_data['status'].append('fallen')
                timeline_data['current_streak'] = 0

        # Calcular posição média (ignorando Nones)
        valid_positions = [p for p in timeline_data['positions'] if p is not None]
        if valid_positions:
            timeline_data['avg_position'] = sum(valid_positions) / len(valid_positions)

        crypto_timeline[crypto] = timeline_data

    return {
        'timeline': snapshot_timeline,
        'crypto_data': crypto_timeline,
        'total_snapshots': len(snapshot_timeline),
        'historical_top10': list(historical_top10)
    }

def determine_evolution_status(symbol, historical_data, current_periods):
    """Determina status evolutivo da crypto"""

    if symbol not in historical_data['crypto_data']:
        return 'unknown'

    crypto_info = historical_data['crypto_data'][symbol]

    # Critérios de status
    if crypto_info['total_appearances'] == 0:
        return 'unknown'
    elif crypto_info['total_appearances'] == 1:
        return 'newcomer'
    elif crypto_info['current_streak'] >= 5:
        return 'consistent'
    elif crypto_info['current_streak'] >= 3:
        return 'rising'
    elif crypto_info['current_streak'] == 0:
        return 'fallen'
    else:
        return 'stable'

def create_evolution_timeline(historical_data, snapshot_info):
    """Cria HTML da timeline interativa"""

    if not historical_data:
        return "<div><p>⚠️ Dados históricos não disponíveis</p></div>"

    timeline = historical_data['timeline']
    crypto_data = historical_data['crypto_data']

    # Identificar entradas e saídas recentes
    recent_entries = []
    recent_exits = []

    if len(timeline) >= 2:
        current_top10 = set(timeline[-1]['top10_symbols'])
        previous_top10 = set(timeline[-2]['top10_symbols'])

        recent_entries = list(current_top10 - previous_top10)
        recent_exits = list(previous_top10 - current_top10)

    timeline_html = f"""
    <div class="stats">
        <h4>📅 TIMELINE EVOLUTIVA - Últimos {len(timeline)} Períodos</h4>

        <div style="margin-bottom: 20px;">
            <h5>🔥 ENTRADAS RECENTES:</h5>
            {''.join([f'<span style="display: inline-block; margin: 5px; padding: 5px 10px; background: #2ecc71; color: white; border-radius: 5px;">{crypto}</span>' for crypto in recent_entries]) if recent_entries else '<span style="color: #666;">Nenhuma entrada recente</span>'}
        </div>

        <div style="margin-bottom: 20px;">
            <h5>📤 SAÍDAS RECENTES:</h5>
            {''.join([f'<span style="display: inline-block; margin: 5px; padding: 5px 10px; background: #e74c3c; color: white; border-radius: 5px;">{crypto}</span>' for crypto in recent_exits]) if recent_exits else '<span style="color: #666;">Nenhuma saída recente</span>'}
        </div>

        <div style="margin-bottom: 20px;">
            <h5>📊 ESTATÍSTAS EVOLUTIVAS:</h5>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                <div style="text-align: center; padding: 10px; background: #ecf0f1; border-radius: 5px;">
                    <strong>{len(historical_data['historical_top10'])}</strong><br>
                    <small>Total Cryptos no TOP 10 (Histórico)</small>
                </div>
                <div style="text-align: center; padding: 10px; background: #ecf0f1; border-radius: 5px;">
                    <strong>{len(timeline)}</strong><br>
                    <small>Períodos Analisados</small>
                </div>
                <div style="text-align: center; padding: 10px; background: #ecf0f1; border-radius: 5px;">
                    <strong>{len([c for c in crypto_data.values() if c['current_streak'] > 0])}</strong><br>
                    <small>Atuais no TOP 10</small>
                </div>
            </div>
        </div>

        <div>
            <h5>👑 CRYPTOS MAIS CONSISTENTES:</h5>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #3498db; color: white;">
                    <th style="padding: 8px; text-align: left;">Crypto</th>
                    <th style="padding: 8px; text-align: center;">Aparições</th>
                    <th style="padding: 8px; text-align: center;">Maior Sequência</th>
                    <th style="padding: 8px; text-align: center;">Posição Média</th>
                    <th style="padding: 8px; text-align: center;">Status</th>
                </tr>
                {''.join([
                    f'''
                    <tr>
                        <td style="padding: 8px;"><strong>{symbol}</strong></td>
                        <td style="padding: 8px; text-align: center;">{data['total_appearances']}</td>
                        <td style="padding: 8px; text-align: center;">{data['max_consecutive']} dias</td>
                        <td style="padding: 8px; text-align: center;">{data['avg_position']:.1f}</td>
                        <td style="padding: 8px; text-align: center;">
                            <span style="color: {'#27ae60' if data['current_streak'] > 0 else '#e74c3c'};">
                                {'👑 Ativa' if data['total_appearances'] == len(timeline) else '📤 Fora'}
                            </span>
                        </td>
                    </tr>
                    '''
                    for symbol, data in sorted(crypto_data.items(),
                        key=lambda x: (
                            0 if x[1]['total_appearances'] == len(timeline) else 1,  # Status: Ativas primeiro
                            -x[1]['total_appearances'],            # Aparições: maior para menor
                            round(x[1]['avg_position'])           # Posição: crescente
                        ))[:10]
                ])}
            </table>
        </div>
    </div>
    """

    return timeline_html

def create_hall_of_fame(historical_data, snapshot_info):
    """Cria HTML do Hall da Fama e das Saídas"""

    if not historical_data:
        return "<div><p>⚠️ Dados históricos não disponíveis</p></div>"

    crypto_data = historical_data['crypto_data']
    crypto_ranking = historical_data.get('crypto_ranking', [])

    score_by_symbol = {item.get('symbol'): float(item.get('avg_score', 0) or 0) for item in crypto_ranking if item.get('symbol')}

    def _pick_record_max_consecutive():
        best_symbol = 'N/A'
        best_value = 0
        best_score = -1.0
        for symbol, data in crypto_data.items():
            value = int(data.get('max_consecutive', 0) or 0)
            score = score_by_symbol.get(symbol, 0.0)
            if (value > best_value) or (value == best_value and score > best_score):
                best_symbol = symbol
                best_value = value
                best_score = score
        return best_symbol, best_value

    def _pick_record_most_appearances():
        best_symbol = 'N/A'
        best_value = 0
        best_score = -1.0
        for symbol, data in crypto_data.items():
            value = int(data.get('total_appearances', 0) or 0)
            score = score_by_symbol.get(symbol, 0.0)
            if (value > best_value) or (value == best_value and score > best_score):
                best_symbol = symbol
                best_value = value
                best_score = score
        return best_symbol, best_value

    record_max_streak_symbol, record_max_streak_value = _pick_record_max_consecutive()
    record_most_appear_symbol, record_most_appear_value = _pick_record_most_appearances()

    # Separar cryptos por status
    current_top10 = [s for s, d in crypto_data.items() if d['current_streak'] > 0]
    fallen_heroes = [s for s, d in crypto_data.items() if d['current_streak'] == 0 and d['total_appearances'] >= 3]
    rising_stars = [s for s, d in crypto_data.items() if 1 <= d['current_streak'] < 3 and d['total_appearances'] >= 2]

    hall_html = f"""
    <div class="stats">
        <h4>🏆 HALL DA FAMA EVOLUTIVO</h4>

        <div style="margin-bottom: 20px;">
            <h5>👑 ATUAIS NO TOP 10:</h5>
            <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                {''.join([
                    f'<span style="padding: 5px 10px; background: #3498db; color: white; border-radius: 5px; font-size: 12px;">{crypto} ({crypto_data[crypto]["current_streak"]}🔥)</span>'
                    for crypto in sorted(current_top10, key=lambda x: crypto_data[x]['current_streak'], reverse=True)
                ]) if current_top10 else '<span style="color: #666;">Nenhuma crypto no TOP 10</span>'}
            </div>
        </div>

        <div style="margin-bottom: 20px;">
            <h5>📤 HERÓIS CAÍDOS (Foram TOP 10+ vezes):</h5>
            <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                {''.join([
                    f'<span style="padding: 5px 10px; background: #e74c3c; color: white; border-radius: 5px; font-size: 12px;">{crypto} ({crypto_data[crypto]["total_appearances"]}x)</span>'
                    for crypto in sorted(fallen_heroes, key=lambda x: crypto_data[x]['total_appearances'], reverse=True)[:15]
                ]) if fallen_heroes else '<span style="color: #666;">Nenhum herói caído</span>'}
            </div>
        </div>

        <div style="margin-bottom: 20px;">
            <h5>🌟 ESTRELAS EM ASCENSÃO:</h5>
            <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                {''.join([
                    f'<span style="padding: 5px 10px; background: #f39c12; color: white; border-radius: 5px; font-size: 12px;">{crypto} ({crypto_data[crypto]["current_streak"]}🔥)</span>'
                    for crypto in sorted(rising_stars, key=lambda x: crypto_data[x]['current_streak'], reverse=True)[:10]
                ]) if rising_stars else '<span style="color: #666;">Nenhuma estrela em ascensão</span>'}
            </div>
        </div>

        <div>
            <h5>📊 RECORDS HISTÓRICOS:</h5>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #3498db; color: white;">
                    <th style="padding: 8px; text-align: left;">Record</th>
                    <th style="padding: 8px; text-align: left;">Crypto</th>
                    <th style="padding: 8px; text-align: center;">Valor</th>
                </tr>
                <tr>
                    <td style="padding: 8px;">👑 Maior Sequência</td>
                    <td style="padding: 8px;">
                        {record_max_streak_symbol}
                    </td>
                    <td style="padding: 8px; text-align: center;">
                        {record_max_streak_value} dias
                    </td>
                </tr>
                <tr>
                    <td style="padding: 8px;">📈 Mais Aparições</td>
                    <td style="padding: 8px;">
                        {record_most_appear_symbol}
                    </td>
                    <td style="padding: 8px; text-align: center;">
                        {record_most_appear_value} vezes
                    </td>
                </tr>
                <tr>
                    <td style="padding: 8px;">🎯 Melhor Posição Média</td>
                    <td style="padding: 8px;">
                        {min(crypto_data.items(), key=lambda x: x[1]['avg_position'] if x[1]['avg_position'] > 0 else 999)[0]}
                    </td>
                    <td style="padding: 8px; text-align: center;">
                        {min([d['avg_position'] for d in crypto_data.values() if d['avg_position'] > 0]):.1f}
                    </td>
                </tr>
            </table>
        </div>
    </div>
    """

    return hall_html

def get_evolution_color(evolution_status):
    """Retorna cor baseada no status evolutivo"""
    colors = {
        'consistent': '#27ae60',    # Verde
        'rising': '#3498db',        # Azul
        'stable': '#f39c12',       # Laranja
        'fallen': '#e74c3c',        # Vermelho
        'newcomer': '#9b59b6',      # Roxo
        'unknown': '#95a5a6'       # Cinza
    }
    return colors.get(evolution_status, '#95a5a6')

def get_evolution_emoji(evolution_status):
    """Retorna emoji baseado no status evolutivo"""
    emojis = {
        'consistent': '👑',
        'rising': '🚀',
        'stable': '➡️',
        'fallen': '📉',
        'newcomer': '🆕',
        'unknown': '❓'
    }
    return emojis.get(evolution_status, '❓')
