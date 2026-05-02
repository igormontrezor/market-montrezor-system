"""
Exemplo básico de uso do sistema de análise de mercado
"""

from market_analyze.assets import Crypto, YahooProvider
from market_analyze.indicators import SimpleMovingAverage, Rsi, Macd
from market_analyze.signals import RsiSignal, BollingerBandsSignal, CombinedSignal
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

    # Bollinger Bands
    bb = BollingerBands(period=20, std_dev=2)
    btc_bb = bb.calculate(btc)

    print(f"BTC RSI Atual: {btc_rsi.iloc[-1]:.2f}")
    print(f"BTC Bollinger Bands Atual: {btc_bb['upper'].iloc[-1]:.2f}")

    # Gerar sinais
    print("\n=== Gerando Sinais ===")

    # Sinal RSI
    rsi_signal = RsiSignal(rsi=rsi, buy_threshold=20, sell_threshold=80)
    btc_rsi_signals = rsi_signal.generate_signals(btc)

    # Sinal Bollinger Bands
    bb_signal = BollingerBandsSignal(bb=bb)
    btc_bb_signals = bb_signal.generate_signals(btc)

    # Sinal combinado
    combined_signal = CombinedSignal(
        signals=[rsi_signal, bb_signal],
        weights=[0.5, 1.5],
        quantity_threshold=2.0,
        window=2
    )
    btc_combined_signals = combined_signal.confirm_signals(btc)

    # Contar sinais
    rsi_buy_count = (btc_rsi_signals == -1).sum()
    rsi_sell_count = (btc_rsi_signals == 1).sum()
    bb_buy_count = (btc_bb_signals == -1).sum()
    bb_sell_count = (btc_bb_signals == 1).sum()
    combined_buy_count = (btc_combined_signals == -1).sum()
    combined_sell_count = (btc_combined_signals == 1).sum()

    print(f"RSI - Compras: {rsi_buy_count}, Vendas: {rsi_sell_count}")
    print(f"Bollinger Bands - Compras: {bb_buy_count}, Vendas: {bb_sell_count}")
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
