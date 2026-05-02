"""
📱 CONFIGURAÇÃO TELEGRAM PARA SCRAPING REAL

Para ativar scraping real do Telegram, siga estes passos:

1. INSTALAR TELETHON:
   pip install telethon

2. OBTER CREDENCIAIS:
   - Vá para: https://my.telegram.org/
   - Faça login com seu número de telefone
   - Crie uma nova aplicação
   - Copie api_id e api_hash

3. CONFIGURAR VARIÁVEIS:
   - Preencha suas credenciais abaixo
   - O sistema usará dados reais automaticamente

4. PRIMEIRO USO:
   - Execute o sistema uma vez para autenticar
   - Telethon pedirá seu número e código de verificação
   - Session será salva para usos futuros

⚠️ IMPORTANTE:
- Use um número de telefone dedicado para automação
- Respeite os rate limits do Telegram
- Canais privados não serão acessíveis
"""

# 🔧 PREENCHA SUAS CREDENCIAIS AQUI:
TELEGRAM_API_ID = None  # Seu api_id (número inteiro)
TELEGRAM_API_HASH = None  # Seu api_hash (string)
TELEGRAM_PHONE = None  # Seu número de telefone (formato: +55XXYYYYYYYY)

# 📱 CANAIS PARA MONITORAR (já configurados no sistema)
TELEGRAM_CHANNELS = [
    'cryptochat',           # Peso: 1.0 (padrão)
    'crypto_signals',       # Peso: 0.5 (menos confiável)
    'altcoin_trading',     # Peso: 0.8 (confiável)
    'cryptocurrency_news'   # Peso: 1.5 (muito confiável)
]

# ⚖️ PESOS POR CANAL (qualidade das menções)
CHANNEL_WEIGHTS = {
    'cryptochat': 1.0,           # Canal padrão
    'crypto_signals': 0.5,       # Sinais comerciais (menos peso)
    'altcoin_trading': 0.8,       # Comunidade ativa
    'cryptocurrency_news': 1.5   # Notícias (maior peso)
}

# 🚀 CONFIGURAÇÕES DE SCRAPING
SCRAPING_CONFIG = {
    'max_messages_per_channel': 100,  # Limite de mensagens por canal
    'rate_limit_delay': 1.0,          # Segundos entre canais
    'search_days': 7,                 # Dias para buscar
    'min_mentions_threshold': 1       # Mínimo de menções para considerar
}

# ✅ STATUS DA CONFIGURAÇÃO
def is_configured():
    """Verifica se as credenciais estão configuradas"""
    return all([TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE])

def get_config_status():
    """Retorna status da configuração"""
    if is_configured():
        return "✅ Telegram configurado para scraping real"
    else:
        return "⚠️ Telegram não configurado (usando simulação)"

if __name__ == "__main__":
    print(get_config_status())
    print("\n📋 Canais configurados:")
    for channel in TELEGRAM_CHANNELS:
        weight = CHANNEL_WEIGHTS.get(channel, 1.0)
        print(f"  - {channel} (peso: {weight})")

    if not is_configured():
        print("\n🔧 Para configurar:")
        print("1. Edite este arquivo")
        print("2. Preencha TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE")
        print("3. Execute: pip install telethon")
        print("4. O sistema usará dados reais automaticamente")
