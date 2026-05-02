#!/usr/bin/env python3
"""
🧠 SOCIAL ANALYZER v2.0 - YouTube + Telegram
Camada 4: Confirmação de Atenção (não detecção)
Social como validação, não como filtro primário
"""

import requests
import json
import os
import re
import math
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List
import time

# Importar configuração local
from config import YOUTUBE_API_KEY

class SocialAnalyzerYTTelegram:
    def __init__(self):
        # APIs (gratuitas)
        self.youtube_api_key = YOUTUBE_API_KEY  # YouTube Data API v3
        self.telegram_channels = [
            'cryptochat',
            'crypto_signals',
            'altcoin_trading',
            'cryptocurrency_news'
        ]

        # 🔥 Pesos por canal para filtrar qualidade
        self.channel_weights = {
            'cryptochat': 1.0,           # Discussão geral - peso neutro
            'crypto_signals': 0.5,        # Sinais - menor peso (possível spam)
            'altcoin_trading': 0.8,       # Trading - peso moderado
            'cryptocurrency_news': 1.5    # Notícias - maior peso (qualidade)
        }

        # Cache para evitar requisições excessivas
        self.cache = {}
        self.cache_duration = timedelta(hours=1)

    def check_social_validation(self, symbol: str, ratio: float, strong_days: int, name: str = None) -> Dict[str, Any]:
        """
        🔥 CAMADA 4: Confirmação Social
        Só analisa social SE já tiver sinais técnicos fortes
        """

        # 🎯 Critério principal: Só analisa com sinais fortes (AJUSTADO)
        if ratio < 0.5 or strong_days < 1:
            return {
                'should_analyze': False,
                'reason': 'Sinais técnicos insuficientes para validação social',
                'youtube_velocity': 0,
                'telegram_spike': 0,
                'combined_validation': 'NOT_APPLICABLE'
            }

        # 🎯 Usar nome completo se disponível, senão símbolo
        search_term = name if name else symbol

        # 🚀 Se passou no filtro técnico, analisa social
        print(f"🧠 {symbol}: Sinais técnicos fortes (ratio: {ratio:.2f}, dias: {strong_days}) → Validando social...")

        # 📊 Obter dados sociais usando nome completo (apenas YouTube)
        youtube_data = self.get_youtube_metrics(symbol, name)
        telegram_data = self.get_telegram_metrics(search_term)  # Mantém coleta mas não usa no cálculo

        # Calcular métricas essenciais (apenas YouTube)
        youtube_velocity = self.calculate_youtube_velocity(youtube_data)
        telegram_spike = 0.0  # Telegram ignorado no cálculo

        # ✅ VERIFICAÇÃO DE QUALIDADE DE DADOS - Apenas YouTube
        youtube_quality = youtube_data.get('data_source', 'unknown')

        # ✅ PENALIZAÇÃO PARA DADOS SIMULADOS - Apenas YouTube
        if youtube_quality == 'simulation':
            youtube_velocity *= 0.7  # Penalização de 30%
            print(f"⚠️ {symbol}: YouTube dados simulados - velocity penalizada (-30%)")

        # Validação baseada apenas no YouTube
        validation = self.get_youtube_only_validation(youtube_velocity)

        return {
            'should_analyze': True,
            'reason': 'Validação social completa',
            'youtube_velocity': youtube_velocity,
            'telegram_spike': telegram_spike,
            'combined_validation': validation,
            'youtube_data': youtube_data,
            'telegram_data': telegram_data,
            # ✅ FLAGS DE QUALIDADE - Transparência total sobre origem dos dados
            'youtube_data_quality': youtube_quality,
            'telegram_data_quality': telegram_quality,
            'data_quality_warning': (youtube_quality == 'simulation' or telegram_quality == 'simulation'),
            'both_simulated': (youtube_quality == 'simulation' and telegram_quality == 'simulation')
        }

    def get_youtube_metrics(self, symbol: str, name: str = None) -> Dict[str, Any]:
        """
        📺 Coleta métricas do YouTube (API REAL implementada)
        Cache centralizado para evitar duplicação
        """
        # ✅ CORREÇÃO: Cache key único inclui name para evitar compartilhamento incorreto
        cache_key = f"youtube_{symbol}_{name or 'none'}"

        # ✅ CACHE CENTRALIZADO - Verificar apenas uma vez
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if datetime.now(timezone.utc) - cached_time < self.cache_duration:
                return cached_data

        # 🚀 IMPLEMENTAÇÃO REAL COM YouTube API
        if self.youtube_api_key:
            try:
                # Tentar busca real primeiro
                real_data = self._fetch_youtube_metrics_real(symbol, name)
                # ✅ CORREÇÃO: Usar dados reais mesmo sem vídeos hoje (evitar simulação desnecessária)
                if real_data.get('total_videos_found', 0) > 0:
                    print(f"📺 {symbol}: {real_data['today_videos']} vídeos hoje (total: {real_data.get('total_videos_found', 0)})")
                    # Salvar no cache (único lugar)
                    self.cache[cache_key] = (datetime.now(timezone.utc), real_data)
                    return real_data
                else:
                    print(f"📺 {symbol}: Nenhum vídeo encontrado, usando simulação")
            except Exception as e:
                print(f"📺 {symbol}: Erro na API YouTube, usando simulação - {e}")

        # Fallback para simulação
        simulated_data = self.simulate_youtube_data(symbol)
        print(f"📺 {symbol}: Usando dados simulados ({simulated_data['today_videos']} vídeos hoje)")

        # Salvar no cache (único lugar)
        self.cache[cache_key] = (datetime.now(timezone.utc), simulated_data)

        return simulated_data

    def _fetch_youtube_metrics_real(self, symbol: str, name: str = None) -> Dict[str, Any]:
        """
        🔧 FUNÇÃO INTERNA - Busca métricas REAIS do YouTube (sem cache)
        Cache gerenciado pelo método principal get_youtube_metrics()
        """

        # 🚀 IMPLEMENTAÇÃO REAL COM YouTube API
        try:
            # ✅ MELHOR: Usar nome completo quando disponível
            search_term = name if name else symbol

            # ✅ MELHOR: Query específica com aspas para reduzir ruído
            url = f"https://www.googleapis.com/youtube/v3/search"

            # ✅ CORREÇÃO: Escapar aspas e caracteres especiais no search_term
            clean_term = search_term.replace('"', '').replace("'", "").strip()
            if not clean_term:
                # Fallback para symbol se name estiver vazio após limpeza
                clean_term = symbol.replace('"', '').replace("'", "").strip()

            params = {
                'part': 'snippet',
                'q': f'"{clean_term}" crypto OR "{clean_term}" token',
                'type': 'video',
                'maxResults': 50,
                'publishedAfter': (datetime.now(timezone.utc) - timedelta(days=7)).isoformat().replace('+00:00', 'Z'),
                'key': self.youtube_api_key
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return self.process_youtube_data(response.json(), symbol)
            else:
                print(f"❌ Erro API YouTube: {response.status_code}")
                return self.simulate_youtube_data(symbol)
        except Exception as e:
            print(f"❌ Erro API YouTube: {e}")
            return self.simulate_youtube_data(symbol)

    def process_youtube_data(self, youtube_response: Dict, symbol: str) -> Dict[str, Any]:
        """
        📊 Processa dados reais da YouTube API (CORRIGIDO - 2 chamadas)
        """
        import random
        from collections import defaultdict

        videos = youtube_response.get('items', [])

        # 🚀 CORREÇÃO CRÍTICA: Extrair IDs dos vídeos da primeira chamada (search)
        video_ids = []
        daily_videos_count = defaultdict(int)

        for video in videos:
            # Extrair ID do vídeo
            video_id = video.get('id', {}).get('videoId')
            if video_id:
                video_ids.append(video_id)

            # Agrupar por data de publicação
            snippet = video.get('snippet', {})
            published_at = snippet.get('publishedAt', '')

            if published_at:
                video_date = published_at[:10]  # YYYY-MM-DD
                daily_videos_count[video_date] += 1

        # 🚀 SEGUNDA CHAMADA: Buscar statistics reais dos vídeos
        total_views = 0
        total_likes = 0
        total_comments = 0
        video_count = 0

        if video_ids:
            try:
                # Buscar statistics usando endpoint videos
                videos_url = "https://www.googleapis.com/youtube/v3/videos"
                videos_params = {
                    'part': 'statistics',
                    'id': ','.join(video_ids),
                    'key': self.youtube_api_key
                }

                videos_response = requests.get(videos_url, params=videos_params, timeout=10)
                if videos_response.status_code == 200:
                    videos_data = videos_response.json()

                    # Processar statistics reais
                    for video in videos_data.get('items', []):
                        statistics = video.get('statistics', {})
                        views = int(statistics.get('viewCount', 0))
                        likes = int(statistics.get('likeCount', 0))
                        comments = int(statistics.get('commentCount', 0))

                        total_views += views
                        total_likes += likes
                        total_comments += comments
                        video_count += 1

                    print(f"📊 {symbol}: {video_count} vídeos com statistics reais")
                else:
                    print(f"❌ Erro API videos: {videos_response.status_code}")

            except Exception as e:
                print(f"❌ Erro buscando statistics: {e}")

        # Criar array dos últimos 7 dias (hoje = índice 0)
        daily_videos = []
        for i in range(7):
            date = (datetime.now(timezone.utc) - timedelta(days=i)).strftime('%Y-%m-%d')
            count = daily_videos_count.get(date, 0)
            daily_videos.append(count)

        # ✅ MELHOR: Calcular média 7 dias (excluindo hoje)
        videos_except_today = daily_videos[1:]
        avg_7d = sum(videos_except_today) / len(videos_except_today) if videos_except_today else 0

        # Médias por vídeo (com dados reais quando disponíveis)
        if video_count > 0:
            avg_views = total_views / video_count
            avg_likes = total_likes / video_count
            avg_comments = total_comments / video_count
            print(f"📈 {symbol}: Views médios: {avg_views:,.0f}, Likes: {avg_likes:.0f}, Comments: {avg_comments:.0f}")
        else:
            # Fallback para valores simulados se não conseguiu statistics
            avg_views = random.randint(1000, 50000)
            avg_likes = random.randint(50, 500)
            avg_comments = random.randint(5, 100)
            print(f"📈 {symbol}: Usando engagement simulado (sem statistics)")

        return {
            'symbol': symbol,
            'daily_videos': daily_videos,
            'today_videos': daily_videos[0],
            'avg_7d_videos': avg_7d,
            'avg_views_per_video': avg_views,
            'avg_likes_per_video': avg_likes,
            'avg_comments_per_video': avg_comments,
            'total_engagement': avg_likes + avg_comments,
            'total_videos_found': len(videos),
            'videos_with_stats': video_count,
            'data_source': 'real' if video_count > 0 else 'simulation'
        }

    def simulate_youtube_data(self, symbol: str) -> Dict[str, Any]:
        """
        🎯 Simulação de dados YouTube (fallback)
        """
        import random

        # Symbols populares têm mais vídeos
        base_activity = {
            'btc': 50, 'eth': 40, 'bnb': 30,
            'ada': 25, 'sol': 20, 'dot': 15,
            'avax': 12, 'matic': 18, 'link': 10
        }

        base_videos = base_activity.get(symbol.lower(), random.randint(5, 15))

        # Simular últimos 7 dias
        daily_videos = []
        for i in range(7):
            # Variação natural com possível spike
            videos = base_videos + random.randint(-3, 10)
            if i == 0:  # Hoje pode ter spike
                videos = max(videos, random.randint(base_videos, base_videos * 5))
            daily_videos.append(max(videos, 1))

        # ✅ MELHOR: Calcular média 7 dias (excluindo hoje)
        videos_except_today = daily_videos[1:]
        avg_7d = sum(videos_except_today) / len(videos_except_today) if videos_except_today else 0

        # Engagement médio por vídeo
        avg_views = random.randint(1000, 50000)
        avg_likes = random.randint(50, 500)
        avg_comments = random.randint(5, 100)

        return {
            'symbol': symbol,
            'daily_videos': daily_videos,
            'today_videos': daily_videos[0],
            'avg_7d_videos': avg_7d,
            'avg_views_per_video': avg_views,
            'avg_likes_per_video': avg_likes,
            'avg_comments_per_video': avg_comments,
            'total_engagement': avg_likes + avg_comments,
            'data_source': 'simulation'
        }

    def get_telegram_metrics(self, symbol: str) -> Dict[str, Any]:
        """
        📱 Coleta métricas do Telegram (scraping gratuito)
        """
        cache_key = f"telegram_{symbol}"

        # Verificar cache
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if datetime.now(timezone.utc) - cached_time < self.cache_duration:
                return cached_data

        # 🚀 IMPLEMENTAÇÃO REAL (scraping Telegram)
        try:
            # Buscar menções em canais públicos usando Telethon
            mentions_today = 0
            mentions_7d = 0

            weighted_mentions_today = 0
            weighted_mentions_7d = 0
            successful_channels = 0
            successful_channel_weights = []  # ✅ CORREÇÃO: Rastrear pesos dos canais bem-sucedidos

            for channel in self.telegram_channels:
                # 🔥 Aplicar peso por canal para filtrar qualidade
                weight = self.channel_weights.get(channel, 1.0)

                try:
                    # Scraping real do canal
                    channel_data = self.scrape_telegram_channel_real(channel, symbol)

                    if channel_data:
                        # Aplicar peso às menções
                        weighted_mentions_today += channel_data['today'] * weight
                        weighted_mentions_7d += channel_data['week_total'] * weight
                        successful_channels += 1
                        successful_channel_weights.append(weight)  # ✅ Rastrear peso deste canal
                        print(f"📱 {channel}: {channel_data['today']} menções hoje")
                    else:
                        print(f"📱 {channel}: Canal privado ou sem acesso")

                except Exception as e:
                    print(f"📱 {channel}: Erro no scraping - {e}")
                    continue

            # 🔥 Retornar menções ponderadas (qualidade filtrada)
            if successful_channels > 0:
                # ✅ CORREÇÃO: Usar peso total apenas dos canais que tiveram sucesso
                total_weight = sum(successful_channel_weights) if successful_channel_weights else successful_channels

                if total_weight > 0:
                    normalized_mentions_today = weighted_mentions_today / total_weight
                    # ✅ CORREÇÃO: weighted_mentions_7d é total semanal, converter para média diária
                    weekly_total = weighted_mentions_7d / total_weight
                    normalized_mentions_7d_avg = weekly_total / 7  # Média diária
                else:
                    normalized_mentions_today = weighted_mentions_today / successful_channels
                    normalized_mentions_7d_avg = (weighted_mentions_7d / successful_channels) / 7
            else:
                # Fallback para simulação se nenhum canal funcionou
                print(f"📱 {symbol}: Nenhum canal acessível, usando simulação")
                return self.simulate_telegram_data(symbol)

            print(f"📱 {symbol}: {successful_channels}/{len(self.telegram_channels)} canais analisados")

            return {
                'symbol': symbol,
                'mentions_today': max(normalized_mentions_today, 1),  # Mínimo 1 para evitar zero
                'mentions_7d_avg': max(normalized_mentions_7d_avg, 1),  # Mínimo 1
                'channels_analyzed': len(self.telegram_channels),
                'successful_channels': successful_channels,
                'data_source': 'real'
            }
        except Exception as e:
            print(f"❌ Erro scraping Telegram: {e}")
            # Fallback para simulação
            return self.simulate_telegram_data(symbol)

        # IMPLEMENTAÇÃO SIMULADA
        simulated_data = self.simulate_telegram_data(symbol)

        # Salvar no cache
        self.cache[cache_key] = (datetime.now(timezone.utc), simulated_data)

        return simulated_data

    def scrape_telegram_channel_real(self, channel: str, symbol: str) -> Optional[Dict[str, Any]]:
        """
        📱 Scraping real do Telegram usando Telethon
        """
        try:
            from telethon.sync import TelegramClient
            from telethon.tl.functions.messages import GetHistoryRequest
            from telethon.tl.types import InputPeerEmpty
            from collections import defaultdict
            import asyncio

            # Configuração do cliente (importar do arquivo de config)
            try:
                from telegram_config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE

                if not all([TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE]):
                    print(f"📱 {channel}: Configuração Telegram incompleta")
                    return None

                api_id, api_hash, phone = TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE

            except ImportError:
                print(f"📱 {channel}: Arquivo telegram_config.py não encontrado")
                return None

            # Criar cliente (em modo síncrono para simplicidade)
            client = TelegramClient('session_name', api_id, api_hash)

            # Buscar menções do símbolo nos últimos 7 dias no canal específico
            seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

            # ✅ CORREÇÃO: Busca no canal específico (não global)
            try:
                # Obter entidade do canal
                channel_entity = client.get_entity(channel)

                # Buscar histórico do canal
                results = client(GetHistoryRequest(
                    peer=channel_entity,
                    limit=100,
                    offset_date=seven_days_ago,
                    offset_id=0,
                    max_id=0,
                    min_id=0,
                    add_offset=0,
                    hash=0
                ))

            except Exception as e:
                print(f"📱 {channel}: Erro ao acessar canal - {e}")
                return None

            # Contar menções por dia no canal específico
            daily_mentions = defaultdict(int)
            total_mentions = 0

            for message in results.messages:
                if message.message:
                    # ✅ CORREÇÃO: Regex com boundaries para evitar falsos positivos
                    import re
                    if re.search(rf'\b{re.escape(symbol)}\b', message.message, re.IGNORECASE):
                        message_date = message.date.date()
                        daily_mentions[message_date] += 1
                        total_mentions += 1

            # Calcular menções de hoje e semana
            today = datetime.now(timezone.utc).date()
            today_mentions = daily_mentions.get(today, 0)
            week_total = sum(daily_mentions.get(today - timedelta(days=i), 0) for i in range(7))

            # Rate limit protection
            time.sleep(1)  # 1 segundo entre canais

            print(f"📱 {channel}: {total_mentions} menções de {symbol} (últimos 7 dias)")

            return {
                'today': today_mentions,
                'week_total': week_total,
                'daily_breakdown': dict(daily_mentions),
                'channel_name': channel,
                'messages_analyzed': len(results.messages)
            }

        except ImportError:
            print(f"📱 {channel}: Telethon não instalado. Instale com: pip install telethon")
            return None
        except Exception as e:
            print(f"📱 {channel}: Erro no scraping - {e}")
            return None

    def simulate_telegram_data(self, symbol: str) -> Dict[str, Any]:
        """
        🎯 Simulação de dados Telegram para teste
        """
        import random

        # Base activity por symbol
        base_mentions = {
            'btc': 200, 'eth': 150, 'bnb': 80,
            'ada': 60, 'sol': 70, 'dot': 40,
            'avax': 30, 'matic': 50, 'link': 25
        }

        base = base_mentions.get(symbol.lower(), random.randint(10, 40))

        # Simular menções com possível spike
        today_mentions = base + random.randint(-10, base * 3)
        week_mentions = base * 7 + random.randint(-50, 200)

        return {
            'symbol': symbol,
            'mentions_today': max(today_mentions, 5),
            'mentions_7d_avg': max(week_mentions / 7, 5),
            'channels_analyzed': len(self.telegram_channels),
            'data_source': 'simulation'
        }

    def calculate_youtube_velocity(self, youtube_data: Dict[str, Any]) -> float:
        """
        🔥 YouTube Velocity = Vídeos hoje / média 7 dias
        Métrica essencial que mostra explosão de conteúdo
        """
        today = youtube_data['today_videos']
        avg_7d = youtube_data['avg_7d_videos']

        # ✅ CORREÇÃO: Preservar ranking mesmo com poucos vídeos (0 ≠ 2)
        if today == 0:
            return 0.1  # Valor mínimo para zero vídeos (distingue de 1, 2 vídeos)
        elif today < 3:
            # Escala linear para preservar ranking: 0.1, 0.6, 1.1
            return 0.1 + (today * 0.5)

        if avg_7d == 0:
            return 1.0

        velocity = today / avg_7d
        # ✅ LOG SCALE: Preserva ranking sem distorção (10x vs 50x ficam diferentes)
        velocity = math.log1p(velocity)  # log1p(x) = log(x + 1), evita log(0)
        return velocity

    def calculate_telegram_spike(self, telegram_data: Dict[str, Any]) -> float:
        """
        📱 Telegram Spike = Menções hoje / média 7 dias
        Indica pico de atenção instantânea
        """
        today = telegram_data['mentions_today']
        avg_7d = telegram_data['mentions_7d_avg']

        # 🔧 MIN DATA FILTER: Reduzido para capturar early gems (sinais iniciais preciosos)
        if today < 5:
            return 1.0

        if avg_7d == 0:
            return 1.0

        spike = today / avg_7d
        # ✅ LOG SCALE: Preserva ranking sem distorção (10x vs 50x ficam diferentes)
        spike = math.log1p(spike)  # log1p(x) = log(x + 1), evita log(0)
        return spike

    def get_youtube_only_validation(self, youtube_velocity: float) -> str:
        """
        🎯 Validação social baseada apenas no YouTube
        """
        # 🚀 Explosão social (YouTube muito forte) - ajustado para log scale
        # log1p(3.0) ≈ 1.4
        if youtube_velocity >= 1.4:
            return 'SOCIAL_EXPLOSION'

        # 💪 Atenção forte (YouTube forte) - ajustado para log scale
        # log1p(2.0) ≈ 1.1
        elif youtube_velocity >= 1.1:
            return 'SOCIAL_STRONG'

        # 📊 Atenção moderada (YouTube moderado) - ajustado para log scale
        # log1p(1.3) ≈ 0.85
        elif youtube_velocity >= 0.85:
            return 'SOCIAL_MODERATE'

        # 📈 Atenção baixa (YouTube baixo) - ajustado para log scale
        # log1p(1.2) ≈ 0.8
        elif youtube_velocity >= 0.8:
            return 'SOCIAL_LOW'

        # ❌ Sem atenção social
        else:
            return 'SOCIAL_WEAK'

    def get_combined_validation(self, youtube_velocity: float, telegram_spike: float) -> str:
        """
        🎯 Validação social combinada (mantido para compatibilidade)
        """
        return self.get_youtube_only_validation(youtube_velocity)

    def social_score(self, validation: str) -> int:
        """
        🔢 Score numérico para uso quantitativo (sem alterar lógica)
        Mantém leitura humana + adiciona valor numérico
        """
        return {
            'SOCIAL_EXPLOSION': 3,
            'SOCIAL_STRONG': 2,
            'SOCIAL_MODERATE': 1,
            'SOCIAL_LOW': 0,
            'SOCIAL_WEAK': -1,
            'NOT_APPLICABLE': 0,
            'NO_DATA': 0
        }.get(validation, 0)

    def print_social_analysis(self, symbol: str, result: Dict[str, Any]):
        """
        📊 Imprime análise social formatada
        """
        if not result['should_analyze']:
            print(f"📊 {symbol}: {result['reason']}")
            return

        yt_velocity = result['youtube_velocity']
        tg_spike = result['telegram_spike']
        validation = result['combined_validation']

        # Ícones baseados no resultado
        icons = {
            'SOCIAL_EXPLOSION': '🔥',
            'SOCIAL_STRONG': '💪',
            'SOCIAL_MODERATE': '📊',
            'SOCIAL_LOW': '📈',
            'SOCIAL_WEAK': '❌',
            'NOT_APPLICABLE': '⚠️',
            'NO_DATA': '⚠️'
        }

        icon = icons.get(validation, '📊')

        print(f"{icon} {symbol}: Social {validation.replace('_', ' ')}")
        print(f"   📺 YouTube Velocity: {yt_velocity:.1f}x")
        print(f"   📱 Telegram Spike: {tg_spike:.1f}x")

# Função de teste
def test_social_analyzer():
    """Teste do analisador social YouTube + Telegram"""
    analyzer = SocialAnalyzerYTTelegram()

    # Teste com diferentes cenários
    test_cases = [
        ('BTC', 1.2, 5),    # Forte técnico + social popular
        ('ETH', 0.8, 3),    # Técnico ok + social bom
        ('NEW', 0.9, 4),    # Técnico bom + social desconhecido
        ('WEAK', 0.3, 1),   # Técnico fraco (não deve analisar)
    ]

    print("🧠 TESTE SOCIAL ANALYZER v2.0 - YouTube + Telegram")
    print("=" * 60)

    for symbol, ratio, days in test_cases:
        result = analyzer.check_social_validation(symbol, ratio, days)
        analyzer.print_social_analysis(symbol, result)

if __name__ == "__main__":
    test_social_analyzer()
