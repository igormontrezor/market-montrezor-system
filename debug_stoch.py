import sys
sys.path.append('./src')

from market_analyze.assets import Crypto, YahooProvider
from market_analyze.indicators import StochRsi

# Debug do StochRSI
print("=== DEBUG DO STOCHRSI ===")

# Criar asset
provider = YahooProvider(period="6mo", interval="1wk")
btc = Crypto("BTC-USD", provider=provider)

# Calcular StochRSI
stoch = StochRsi()
stoch_result = stoch.calculate(btc)

print(f"Tipo do resultado: {type(stoch_result)}")
print(f"Shape do resultado: {stoch_result.shape}")
print(f"Colunas do resultado: {stoch_result.columns.tolist()}")
print(f"Índice do resultado: {stoch_result.index[:5]}")

print(f"\nPrimeiras linhas:")
print(stoch_result.head())

print(f"\nÚltimas linhas:")
print(stoch_result.tail())

print(f"\nValores da coluna 'd':")
print(stoch_result['d'].tail())

print(f"\nÚltimo valor da coluna 'd': {stoch_result['d'].iloc[-1]}")
