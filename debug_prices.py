import sys
sys.path.append('./src')

from market_analyze.assets import Crypto, YahooProvider

# Debug dos preços
provider = YahooProvider(period="1mo", interval="1d")
btc = Crypto("BTC-USD", provider=provider)

print("=== DEBUG DOS PREÇOS ===")
df = btc.get_prices()
print(f"Tipo do DataFrame: {type(df)}")
print(f"Colunas: {df.columns.tolist()}")
print(f"Shape: {df.shape}")
print(f"Tipo da coluna Close: {type(df['Close'])}")
print(f"Último valor de Close: {df['Close'].iloc[-1]}")
print(f"Tipo do último valor: {type(df['Close'].iloc[-1])}")

# Verificar se é Series ou valor escalar
last_close = df['Close'].iloc[-1]
if hasattr(last_close, 'iloc'):
    print("É uma Series!")
    print(f"Valores: {last_close.values}")
    print(f"Primeiro valor: {last_close.iloc[0]}")
else:
    print("É um valor escalar")
    print(f"Valor: {last_close}")
