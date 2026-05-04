import pandas as pd

df = pd.read_csv('data/snapshots/gems_10M_to_50M_enhanced_20260503_203107.csv')
print('DADOS RS_24H REAIS:')
for i, row in df.head(10).iterrows():
    rs_24h = row.get('rs_24h', 0)
    print(f'{row["symbol"]:8s} | rs_24h: {rs_24h:6.2f} | Categoria: ', end='')
    if rs_24h >= 1.2:
        print('VERDE FORTE')
    elif rs_24h >= 1.05:
        print('VERDE')
    elif rs_24h >= 0.95:
        print('LARANJA NEUTRO')
    elif rs_24h >= 0.8:
        print('LARANJA FRACO')
    elif rs_24h < 0.8:
        print('VERMELHO MUITO FRACO')
    else:
        print('LARANJA FRACO')
