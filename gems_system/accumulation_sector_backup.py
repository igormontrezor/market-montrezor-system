"""
📈 accumulation_sector.py
Dois módulos complementares ao gems_finder:

1. SilentAccumulationDetector  — detecta padrão de ratio subindo gradualmente
   ao longo de semanas (smart money entrando antes da bull).

2. SectorCorrelationAnalyzer   — agrupa gems por setor e detecta aquecimento
   setorial simultâneo (sinal antecipado de rotação de capital).
"""

import os
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any


# ===========================================================================
# MAPA ESTÁTICO DE SETORES
# Cobre as principais categorias relevantes para gems de small cap.
# Expandir conforme novos projetos aparecerem no sistema.
# ===========================================================================

SECTOR_MAP: Dict[str, str] = {
    # ── Layer 1 / Layer 2 ──────────────────────────────────────────────────
    'sol':    'L1', 'avax': 'L1', 'near': 'L1', 'apt':  'L1',
    'sui':    'L1', 'sei':  'L1', 'ton':  'L1', 'algo': 'L1',
    'one':    'L1', 'ftm':  'L1', 'celo': 'L1', 'kava': 'L1',
    'arb':    'L2', 'op':   'L2', 'matic':'L2', 'pol':  'L2',
    'strk':   'L2', 'zk':   'L2', 'mnt':  'L2', 'metis':'L2',
    'skl':    'L2', 'boba': 'L2', 'celr': 'L2',

    # ── DeFi ───────────────────────────────────────────────────────────────
    'uni':    'DeFi', 'aave': 'DeFi', 'crv':  'DeFi', 'mkr':  'DeFi',
    'comp':   'DeFi', 'snx':  'DeFi', 'bal':  'DeFi', 'sushi':'DeFi',
    'joe':    'DeFi', 'cake': 'DeFi', 'gmx':  'DeFi', 'dydx': 'DeFi',
    'perp':   'DeFi', 'kwenta':'DeFi','radiant':'DeFi','pendle':'DeFi',
    'ldo':    'DeFi', 'rpl':  'DeFi', 'ankr': 'DeFi', 'ssv':  'DeFi',
    'frax':   'DeFi', 'fxs':  'DeFi', 'cvx':  'DeFi', 'yfi':  'DeFi',
    'spell':  'DeFi', 'mim':  'DeFi', 'any':  'DeFi',

    # ── Gaming / GameFi ────────────────────────────────────────────────────
    'axs':    'Gaming', 'sand': 'Gaming', 'mana': 'Gaming', 'enj':  'Gaming',
    'ilv':    'Gaming', 'gala': 'Gaming', 'ygg':  'Gaming', 'mc':   'Gaming',
    'sfp':    'Gaming', 'pgx': 'Gaming',  'prime':'Gaming', 'beam': 'Gaming',
    'magic':  'Gaming', 'gods': 'Gaming', 'guild':'Gaming', 'pyr':  'Gaming',
    'rndr':   'Gaming', 'fet':  'Gaming',

    # ── AI / Data ──────────────────────────────────────────────────────────
    'wld':    'AI', 'ocean': 'AI', 'grt':   'AI', 'agi':  'AI',
    'agix':   'AI', 'numer': 'AI', 'ctxc':  'AI', 'phb':  'AI',
    'aixbt':  'AI', 'bittensor':'AI', 'tao': 'AI', 'io':   'AI',
    'arkm':   'AI', 'kaito': 'AI',

    'rndr':   'Gaming', 'fet':  'Gaming', 'alice': 'Gaming',

    # ── AI / Data ──────────────────────────────────────────────────────────
    'wld':    'AI', 'ocean': 'AI', 'grt':   'AI', 'agi':  'AI',
    'agix':   'AI', 'numer': 'AI', 'ctxc':  'AI', 'phb':  'AI',
    'aixbt':  'AI', 'bittensor':'AI', 'tao': 'AI', 'io':   'AI',
    'arkm':   'AI', 'kaito': 'AI', 'fetc': 'AI', 'fetch': 'AI',

    # ── Meme ───────────────────────────────────────────────────────────────
    'doge':   'Meme', 'shib':    'Meme', 'pepe':     'Meme', 'floki': 'Meme',
    'bonk':   'Meme', 'wif':     'Meme', 'mog':      'Meme', 'turbo': 'Meme',
    'brett':  'Meme', 'popcat':  'Meme', 'chillguy': 'Meme', 'dogs':  'Meme',
    'neiro':  'Meme', 'sundog':  'Meme', 'goat':     'Meme', 'mubarak': 'Meme',
    'broccoli': 'Meme', 'troll': 'Meme', 'bome': 'Meme', 'snek': 'Meme',
    'not':    'Meme', 'giga': 'Meme', 'vine': 'Meme',

    # ── Infrastructure / Oracle ────────────────────────────────────────────
    'link':   'Infra', 'band': 'Infra', 'api3': 'Infra', 'pyth': 'Infra',
    'tel':    'Infra', 'lpt':  'Infra', 'hnt':  'Infra', 'iotx': 'Infra',
    'storj':  'Infra', 'ar':   'Infra', 'fil':  'Infra', 'hot':  'Infra',
    'keep':   'Infra', 'tbtc': 'Infra', 'grt':  'Infra', 'ocean': 'Infra',

    # ── RWA / Stablecoins ──────────────────────────────────────────────────
    'ondo':   'RWA', 'polyx': 'RWA', 'mpl':  'RWA', 'truf': 'RWA',
    'ustc':   'RWA', 'upeg':  'RWA', 'telos':'RWA',

    # ── Privacy ────────────────────────────────────────────────────────────
    'xmr':    'Privacy', 'zec': 'Privacy', 'scrt': 'Privacy', 'rose': 'Privacy',
    'azero':  'Privacy',

    # ── Social / Creator ───────────────────────────────────────────────────
    'deso':   'Social', 'steem':'Social', 'lens': 'Social', 'friend':'Social',
}

def get_sector(symbol: str, coingecko_categories: Optional[List[str]] = None) -> str:
    """
    Retorna o setor de uma crypto.
    Prioridade: mapa estático → categorias CoinGecko → 'Other'
    """
    sym = symbol.lower()
    if sym in SECTOR_MAP:
        return SECTOR_MAP[sym]

    # Fallback via categorias da CoinGecko (quando disponíveis)
    if coingecko_categories:
        cats = [c.lower() for c in coingecko_categories]
        if any('layer-2' in c or 'layer 2' in c for c in cats):
            return 'L2'
        if any('layer-1' in c or 'layer 1' in c for c in cats):
            return 'L1'
        if any('defi' in c or 'decentralized finance' in c for c in cats):
            return 'DeFi'
        if any('gaming' in c or 'gamefi' in c or 'play-to-earn' in c for c in cats):
            return 'Gaming'
        if any('artificial intelligence' in c or 'ai' == c for c in cats):
            return 'AI'
        if any('meme' in c for c in cats):
            return 'Meme'
        if any('real world asset' in c or 'rwa' in c for c in cats):
            return 'RWA'
        if any('privacy' in c for c in cats):
            return 'Privacy'
        if any('oracle' in c or 'infrastructure' in c for c in cats):
            return 'Infra'

    return 'Other'


# ===========================================================================
# 1. DETECTOR DE ACUMULAÇÃO SILENCIOSA
# ===========================================================================

class SilentAccumulationDetector:
    """
    Detecta padrão de ratio subindo gradualmente ao longo de semanas.

    Critérios de acumulação silenciosa:
    ─────────────────────────────────────────────────────────────────
    • Slope positivo consistente no ratio (regressão linear simples)
    • Nenhum spike único > 3x a média (elimina pumps)
    • Presença em pelo menos MIN_SNAPSHOTS períodos
    • Ratio atual acima do ratio médio histórico
    • Aceleração: cada janela de N dias maior que a anterior

    Score de acumulação (0.0 a 1.0):
      0.0–0.3  → sem sinal
      0.3–0.6  → acumulação possível
      0.6–0.8  → acumulação provável
      0.8–1.0  → acumulação forte (smart money)
    """

    MIN_SNAPSHOTS    = 3    # mínimo de pontos para calcular tendência
    SPIKE_MULTIPLIER = 3.0  # ratio acima de N×média = spike (descarta)
    ACCELERATION_WINDOWS = [3, 5]  # janelas para detectar aceleração

    def analyze(self, symbol: str, historical_data: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Analisa acumulação silenciosa para um símbolo.

        Parâmetros
        ----------
        symbol          : símbolo da crypto (ex: 'BTC')
        historical_data : dict {date_str: {symbol: gem_data}} — saída de
                          GemsFinder.load_historical_snapshots()

        Retorna
        -------
        dict com:
          - is_accumulating   : bool — flag principal
          - accumulation_score: float 0–1
          - slope             : float — inclinação do ratio (positivo = subindo)
          - acceleration      : float — aceleração recente vs histórico
          - ratio_series      : list de floats (cronológico)
          - dates             : list de str
          - signal_strength   : str ('none'|'weak'|'moderate'|'strong'|'very_strong')
          - reason            : str explicativo
        """
        result = {
            'is_accumulating':    False,
            'accumulation_score': 0.0,
            'slope':              0.0,
            'acceleration':       0.0,
            'ratio_series':       [],
            'dates':              [],
            'signal_strength':    'none',
            'reason':             'Dados insuficientes'
        }

        # Coletar série temporal do ratio em ordem cronológica
        sorted_dates = sorted(historical_data.keys())
        ratio_series = []
        date_series  = []

        for date in sorted_dates:
            day_data = historical_data[date]
            if symbol in day_data:
                r = day_data[symbol].get('ratio', 0)
                if r > 0:
                    ratio_series.append(r)
                    date_series.append(date)

        result['ratio_series'] = ratio_series
        result['dates']        = date_series

        if len(ratio_series) < self.MIN_SNAPSHOTS:
            result['reason'] = f'Apenas {len(ratio_series)} snapshots (mínimo {self.MIN_SNAPSHOTS})'
            return result

        # ── 1. Slope via regressão linear (sem numpy) ─────────────────────
        n    = len(ratio_series)
        xs   = list(range(n))
        mean_x = sum(xs) / n
        mean_y = sum(ratio_series) / n
        num  = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ratio_series))
        den  = sum((x - mean_x) ** 2 for x in xs)
        slope = num / den if den != 0 else 0.0
        result['slope'] = round(slope, 4)

        # ── 2. Detectar spike (ratio pontual > N×média) ───────────────────
        mean_ratio = mean_y
        max_ratio  = max(ratio_series)
        has_spike  = max_ratio > mean_ratio * self.SPIKE_MULTIPLIER

        # ── 3. Consistência de crescimento ────────────────────────────────
        # Conta quantas transições consecutivas são positivas
        positive_transitions = sum(
            1 for i in range(1, n) if ratio_series[i] > ratio_series[i - 1]
        )
        consistency = positive_transitions / (n - 1)  # 0–1

        # ── 4. Aceleração: média dos últimos W períodos vs média anterior ─
        acceleration = 0.0
        for w in self.ACCELERATION_WINDOWS:
            if n > w:
                recent_mean = sum(ratio_series[-w:]) / w
                older_mean  = sum(ratio_series[:-w]) / len(ratio_series[:-w])
                if older_mean > 0:
                    acc = (recent_mean - older_mean) / older_mean
                    acceleration = max(acceleration, acc)

        result['acceleration'] = round(acceleration, 4)

        # ── 5. Ratio atual acima da média ─────────────────────────────────
        current_above_mean = ratio_series[-1] > mean_ratio

        # ── 6. Score composto ─────────────────────────────────────────────
        score = 0.0

        # Slope positivo: até 0.30
        if slope > 0:
            slope_norm = min(slope / 0.05, 1.0)  # 0.05 por período = saturação
            score += slope_norm * 0.30

        # Consistência de crescimento: até 0.25
        score += consistency * 0.25

        # Aceleração recente: até 0.25
        if acceleration > 0:
            acc_norm = min(acceleration / 0.5, 1.0)  # 50% aceleração = saturação
            score += acc_norm * 0.25

        # Ratio atual acima da média: +0.10
        if current_above_mean:
            score += 0.10

        # Penalidade por spike (sinal de pump, não acumulação)
        if has_spike:
            score *= 0.5
            result['reason'] = 'Spike detectado — possível pump, não acumulação gradual'

        # Penalidade se slope negativo
        if slope < 0:
            score = 0.0
            result['reason'] = 'Ratio em queda — sem acumulação'

        score = round(min(score, 1.0), 3)
        result['accumulation_score'] = score

        # ── 7. Classificar força do sinal ─────────────────────────────────
        if score >= 0.80:
            signal = 'very_strong'
            result['is_accumulating'] = True
            result['reason'] = (
                f'Acumulação silenciosa FORTE: slope={slope:.4f}, '
                f'consistência={consistency*100:.0f}%, aceleração={acceleration*100:.0f}%'
            )
        elif score >= 0.60:
            signal = 'strong'
            result['is_accumulating'] = True
            result['reason'] = (
                f'Acumulação silenciosa: slope={slope:.4f}, '
                f'consistência={consistency*100:.0f}%'
            )
        elif score >= 0.40:
            signal = 'moderate'
            result['is_accumulating'] = False  # Monitorar, não confirmar ainda
            result['reason'] = f'Possível acumulação: slope={slope:.4f}'
        elif score >= 0.20:
            signal = 'weak'
            result['reason'] = f'Sinal fraco: slope={slope:.4f}'
        else:
            signal = 'none'
            if not result['reason']:
                result['reason'] = 'Sem padrão de acumulação'

        result['signal_strength'] = signal
        return result


# ===========================================================================
# 2. ANALISADOR DE CORRELAÇÃO SETORIAL
# ===========================================================================

class SectorCorrelationAnalyzer:
    """
    Detecta aquecimento setorial simultâneo.

    Lógica:
    ───────────────────────────────────────────────────────────────────
    • Para cada snapshot, agrupa gems por setor
    • Calcula ratio médio e contagem de gems "quentes" (ratio ≥ threshold)
      por setor
    • Compara com snapshots anteriores para ver se o setor está
      aquecendo ao longo do tempo
    • Alerta quando 2+ setores distintos aquecem ao mesmo tempo
      (sinal de rotação ampla de capital — antecede bull)

    Níveis de alerta setorial:
      COLD     → ratio médio < 0.3  ou < 2 gems quentes
      WARMING  → ratio médio 0.3–0.5 e 2+ gems quentes
      HOT      → ratio médio 0.5–0.8 e 3+ gems quentes
      BLAZING  → ratio médio ≥ 0.8  e 3+ gems quentes
    """

    HOT_RATIO_THRESHOLD = 0.5   # ratio individual para considerar gem "quente"
    MIN_GEMS_PER_SECTOR = 2     # mínimo de gems por setor para análise válida
    MULTI_SECTOR_ALERT  = 2     # nº de setores HOT+ para disparar alerta geral

    def analyze_snapshot(self, gems: List[Dict]) -> Dict[str, Any]:
        """
        Analisa um único snapshot (lista de gems do dia).

        Retorna dict com métricas por setor e alertas.
        """
        sector_data: Dict[str, List[float]] = {}

        for gem in gems:
            symbol = gem.get('symbol', '').lower()
            cats   = gem.get('categories', [])  # pode vir da CoinGecko
            sector = get_sector(symbol, cats)
            ratio  = gem.get('ratio', 0)
            if ratio <= 0:
                volume = gem.get('total_volume', 0) or 0
                mc     = gem.get('market_cap', 0)
                ratio  = volume / mc if mc > 0 else 0

            if sector not in sector_data:
                sector_data[sector] = []
            sector_data[sector].append(ratio)

        sectors_analysis = {}
        hot_sectors = []

        for sector, ratios in sector_data.items():
            if len(ratios) < self.MIN_GEMS_PER_SECTOR:
                continue

            avg_ratio  = sum(ratios) / len(ratios)
            hot_gems   = sum(1 for r in ratios if r >= self.HOT_RATIO_THRESHOLD)
            max_ratio  = max(ratios)

            # Classificar temperatura
            if avg_ratio >= 0.8 and hot_gems >= 3:
                temp = 'BLAZING'
            elif avg_ratio >= 0.5 and hot_gems >= 3:
                temp = 'HOT'
            elif avg_ratio >= 0.3 and hot_gems >= 2:
                temp = 'WARMING'
            else:
                temp = 'COLD'

            sectors_analysis[sector] = {
                'avg_ratio':   round(avg_ratio, 3),
                'max_ratio':   round(max_ratio, 3),
                'total_gems':  len(ratios),
                'hot_gems':    hot_gems,
                'temperature': temp,
                'ratios':      ratios
            }

            if temp in ('HOT', 'BLAZING'):
                hot_sectors.append(sector)

        # Alerta de rotação ampla
        multi_sector_alert = len(hot_sectors) >= self.MULTI_SECTOR_ALERT

        return {
            'sectors':             sectors_analysis,
            'hot_sectors':         hot_sectors,
            'multi_sector_alert':  multi_sector_alert,
            'alert_level': (
                'ROTATION'  if multi_sector_alert and len(hot_sectors) >= 3 else
                'WARMING'   if multi_sector_alert else
                'SINGLE'    if hot_sectors else
                'COLD'
            )
        }

    def analyze_historical(
        self,
        historical_snapshots: List[Dict],   # lista de {date, gems_list}
    ) -> Dict[str, Any]:
        """
        Analisa tendência setorial ao longo de múltiplos snapshots.

        historical_snapshots: lista ordenada cronologicamente de dicts:
          { 'date': str, 'gems': List[Dict] }

        Retorna:
          - sector_trends: {sector: [{date, avg_ratio, temperature}]}
          - warming_sectors: setores que estão aquecendo (slope positivo)
          - cooling_sectors: setores que estão esfriando
          - current_alert  : alerta do snapshot mais recente
        """
        if not historical_snapshots:
            return {'sector_trends': {}, 'warming_sectors': [], 'cooling_sectors': [], 'current_alert': 'COLD'}

        sector_trends: Dict[str, List[Dict]] = {}

        for snap in historical_snapshots:
            date  = snap.get('date', '')
            gems  = snap.get('gems', [])
            analysis = self.analyze_snapshot(gems)

            for sector, data in analysis['sectors'].items():
                if sector not in sector_trends:
                    sector_trends[sector] = []
                sector_trends[sector].append({
                    'date':        date,
                    'avg_ratio':   data['avg_ratio'],
                    'hot_gems':    data['hot_gems'],
                    'temperature': data['temperature']
                })

        # Calcular slope por setor (regressão linear simples)
        warming_sectors = []
        cooling_sectors = []

        for sector, points in sector_trends.items():
            if len(points) < 2:
                continue
            ratios = [p['avg_ratio'] for p in points]
            n      = len(ratios)
            xs     = list(range(n))
            mean_x = sum(xs) / n
            mean_y = sum(ratios) / n
            num    = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ratios))
            den    = sum((x - mean_x) ** 2 for x in xs)
            slope  = num / den if den != 0 else 0.0

            if slope > 0.01:
                warming_sectors.append({'sector': sector, 'slope': round(slope, 4),
                                        'current_ratio': ratios[-1]})
            elif slope < -0.01:
                cooling_sectors.append({'sector': sector, 'slope': round(slope, 4),
                                        'current_ratio': ratios[-1]})

        warming_sectors.sort(key=lambda x: x['slope'], reverse=True)
        cooling_sectors.sort(key=lambda x: x['slope'])

        # Alerta atual (último snapshot)
        current_alert = 'COLD'
        if historical_snapshots:
            last_gems    = historical_snapshots[-1].get('gems', [])
            last_analysis= self.analyze_snapshot(last_gems)
            current_alert= last_analysis.get('alert_level', 'COLD')

        return {
            'sector_trends':    sector_trends,
            'warming_sectors':  warming_sectors,
            'cooling_sectors':  cooling_sectors,
            'current_alert':    current_alert
        }


# ===========================================================================
# INTEGRAÇÃO COM GemsFinder — funções utilitárias prontas para uso direto
# ===========================================================================

def enrich_gems_with_accumulation(
    gems: List[Dict],
    historical_data: Dict[str, Dict],
    detector: Optional[SilentAccumulationDetector] = None
) -> List[Dict]:
    """
    Adiciona colunas de acumulação silenciosa a cada gem.

    Adiciona:
      - accumulation_score   : float 0–1
      - accumulation_signal  : str ('none'|'weak'|'moderate'|'strong'|'very_strong')
      - accumulation_slope   : float
      - is_silent_accumulation: bool
    """
    if detector is None:
        detector = SilentAccumulationDetector()

    for gem in gems:
        symbol = gem.get('symbol', '')
        result = detector.analyze(symbol, historical_data)
        gem['accumulation_score']    = result['accumulation_score']
        gem['accumulation_signal']   = result['signal_strength']
        gem['accumulation_slope']    = result['slope']
        gem['is_silent_accumulation']= result['is_accumulating']
        gem['accumulation_reason']   = result['reason']

    return gems


def build_sector_snapshot(gems: List[Dict]) -> Dict:
    """
    Monta estrutura { 'date': hoje, 'gems': gems } pronta para o analyzer.
    """
    return {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'gems': gems
    }


def load_sector_historical(
    snapshots_dir: str,
    days: int = 14
) -> List[Dict]:
    """
    Carrega snapshots históricos do disco e monta lista para
    SectorCorrelationAnalyzer.analyze_historical().

    Lê os enhanced CSVs já salvos pelo sistema.
    """
    import glob
    import pandas as pd

    result = []
    pattern = os.path.join(snapshots_dir, '*enhanced_*.csv')
    files   = sorted(glob.glob(pattern))  # cronológico

    # Limitar aos últimos N dias (aprox — cada CSV = 1 execução)
    files = files[-days:]

    for fpath in files:
        try:
            df   = pd.read_csv(fpath)
            gems = df.to_dict(orient='records')
            # Extrair data do nome do arquivo
            fname     = os.path.basename(fpath)
            date_part = fname.split('enhanced_')[1].replace('.csv', '')
            date_str  = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
            result.append({'date': date_str, 'gems': gems})
        except Exception as e:
            print(f"⚠️ Erro ao carregar {fpath}: {e}")

    return result


def print_accumulation_report(gems: List[Dict]) -> None:
    """Imprime relatório de acumulação silenciosa no terminal."""
    accumulators = [g for g in gems if g.get('is_silent_accumulation')]
    monitoring   = [g for g in gems if g.get('accumulation_signal') == 'moderate']

    print("\n📈 DETECÇÃO DE ACUMULAÇÃO SILENCIOSA")
    print("=" * 60)

    if accumulators:
        print(f"\n🟢 CONFIRMADAS ({len(accumulators)}) — smart money provável:")
        for g in sorted(accumulators, key=lambda x: x.get('accumulation_score', 0), reverse=True):
            sig   = g.get('accumulation_signal', 'N/A')
            score = g.get('accumulation_score', 0)
            slope = g.get('accumulation_slope', 0)
            emoji = '🔥' if sig == 'very_strong' else '💚'
            print(f"  {emoji} {g['symbol']:8s} | Score: {score:.2f} | Slope: {slope:+.4f} | {g.get('accumulation_reason','')}")
    else:
        print("\n⚠️ Nenhuma acumulação silenciosa confirmada ainda.")

    if monitoring:
        print(f"\n🟡 MONITORAR ({len(monitoring)}) — possível acumulação:")
        for g in sorted(monitoring, key=lambda x: x.get('accumulation_score', 0), reverse=True):
            print(f"  📊 {g['symbol']:8s} | Score: {g.get('accumulation_score',0):.2f} | {g.get('accumulation_reason','')}")


def print_sector_report(sector_result: Dict) -> None:
    """Imprime relatório de correlação setorial no terminal."""
    print("\n🏭 ANÁLISE SETORIAL")
    print("=" * 60)

    alert = sector_result.get('current_alert', 'COLD')
    alert_emoji = {'ROTATION': '🚨', 'WARMING': '🔥', 'SINGLE': '⚠️', 'COLD': '❄️'}.get(alert, '📊')
    print(f"\n{alert_emoji} ALERTA GERAL: {alert}")

    warming = sector_result.get('warming_sectors', [])
    if warming:
        print(f"\n📈 SETORES AQUECENDO ({len(warming)}):")
        for s in warming:
            print(f"  🌡️  {s['sector']:12s} | Slope: {s['slope']:+.4f} | Ratio atual: {s['current_ratio']:.3f}")

    cooling = sector_result.get('cooling_sectors', [])
    if cooling:
        print(f"\n📉 SETORES ESFRIANDO ({len(cooling)}):")
        for s in cooling[:5]:
            print(f"  🧊 {s['sector']:12s} | Slope: {s['slope']:+.4f} | Ratio atual: {s['current_ratio']:.3f}")

    trends = sector_result.get('sector_trends', {})
    if trends:
        print(f"\n📊 TEMPERATURA ATUAL POR SETOR:")
        # Pegar temperatura do último ponto de cada setor
        rows = []
        for sector, points in trends.items():
            if points:
                last  = points[-1]
                rows.append((sector, last['avg_ratio'], last['temperature'], last['hot_gems']))
        rows.sort(key=lambda x: x[1], reverse=True)
        for sector, avg_r, temp, hot in rows:
            temp_emoji = {'BLAZING': '🔥', 'HOT': '🟠', 'WARMING': '🟡', 'COLD': '❄️'}.get(temp, '📊')
            print(f"  {temp_emoji} {sector:12s} | Ratio médio: {avg_r:.3f} | Gems quentes: {hot} | {temp}")
