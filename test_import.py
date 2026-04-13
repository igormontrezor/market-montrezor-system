import sys
sys.path.append('./src')

try:
    from market_analyze import Crypto, YahooProvider, Rsi
    print("Importação bem-sucedida!")
    
    # Teste básico
    provider = YahooProvider(period="1mo", interval="1d")
    btc = Crypto("BTC-USD", provider=provider)
    print(f"BTC criado com sucesso: {btc.symbol}")
    
    rsi = Rsi(period=14)
    print(f"RSI criado com sucesso: período {rsi.period}")
    
except Exception as e:
    print(f"Erro na importação: {e}")
    import traceback
    traceback.print_exc()
