"""
Exemplo básico de uso do sistema de análise de mercado
"""

from market_analyze.assets import Crypto, YahooProvider
from market_analyze.indicators import SimpleMovingAverage, Rsi, Macd
from market_analyze.signals import RsiSignal, MacdSignal, CombinedSignal
from market_analyze.plotting import ChartPlotter


def main():
    # Criar assets
    btc_provider = YahooProvider(period="2y", interval="1wk")
    btc = Crypto("BTC-USD", provider=btc_provider)
    
    spy_provider = YahooProvider(period="2y", interval="1wk")
    spy = Crypto("SPY", provider=spy_provider)
    
    print("=== Dados dos Ativos ===")
    print(f"BTC Preço Atual: ${btc.get_current_price():.2f}")
    print(f"SPY Preço Atual: ${spy.get_current_price():.2f}")
    
    # Calcular indicadores
    print("\n=== Calculando Indicadores ===")
    
    # SMA
    sma_20 = SimpleMovingAverage(period=20)
    sma_50 = SimpleMovingAverage(period=50)
    
    btc_sma_20 = sma_20.calculate(btc)
    btc_sma_50 = sma_50.calculate(btc)
    
    # RSI
    rsi = Rsi(period=14)
    btc_rsi = rsi.calculate(btc)
    
    # MACD
    macd = Macd()
    btc_macd = macd.calculate(btc)
    
    print(f"BTC RSI Atual: {btc_rsi.iloc[-1]:.2f}")
    print(f"BTC MACD Atual: {btc_macd['macd'].iloc[-1]:.4f}")
    
    # Gerar sinais
    print("\n=== Gerando Sinais ===")
    
    # Sinal RSI
    rsi_signal = RsiSignal(rsi=rsi, buy_threshold=30, sell_threshold=70)
    btc_rsi_signals = rsi_signal.generate_signals(btc)
    
    # Sinal MACD
    macd_signal = MacdSignal(macd=macd)
    btc_macd_signals = macd_signal.generate_signals(btc)
    
    # Sinal combinado
    combined_signal = CombinedSignal(
        signals=[rsi_signal, macd_signal],
        weights=[1.0, 1.0],
        quantity_threshold=2.0,
        window=2
    )
    btc_combined_signals = combined_signal.confirm_signals(btc)
    
    # Contar sinais
    rsi_buy_count = (btc_rsi_signals == -1).sum()
    rsi_sell_count = (btc_rsi_signals == 1).sum()
    macd_buy_count = (btc_macd_signals == 1).sum()
    macd_sell_count = (btc_macd_signals == -1).sum()
    combined_buy_count = (btc_combined_signals == -1).sum()
    combined_sell_count = (btc_combined_signals == 1).sum()
    
    print(f"RSI - Compras: {rsi_buy_count}, Vendas: {rsi_sell_count}")
    print(f"MACD - Compras: {macd_buy_count}, Vendas: {macd_sell_count}")
    print(f"Combinado - Compras: {combined_buy_count}, Vendas: {combined_sell_count}")
    
    # Visualizar dados
    print("\n=== Criando Visualizações ===")
    
    btc_df = btc.get_prices()
    
    # Plotar com sinais combinados
    ChartPlotter.plot_candlestick_with_signals(
        df=btc_df,
        title="BTC-USD com Sinais Combinados",
        buy_signals=btc_combined_signals == -1,
        sell_signals=btc_combined_signals == 1,
        show_volume=True
    )
    
    # Plotar RSI com sinais
    ChartPlotter.plot_indicator_with_signals(
        price_data=btc_df[('Close', 'BTC-USD')] if ('Close', 'BTC-USD') in btc_df.columns else btc_df['Close'],
        indicator_data=btc_rsi,
        title="BTC-USD com RSI",
        buy_signals=btc_rsi_signals == -1,
        sell_signals=btc_rsi_signals == 1,
        indicator_name="RSI (14)"
    )


if __name__ == "__main__":
    main()
