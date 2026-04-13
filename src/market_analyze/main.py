"""
Ponto de entrada principal para o sistema de análise de mercado
"""

import argparse
from typing import Optional

from market_analyze.assets import Crypto, YahooProvider
from market_analyze.indicators import SimpleMovingAverage, Rsi, Macd, StochRsi, SharpeRatio, SortinoRatio
from market_analyze.signals import RsiSignal, MacdSignal, CombinedSignal, StochRsiSignal, SharpeSignal, SortinoSignal
from market_analyze.plotting import ChartPlotter


def main() -> None:
    """Função principal do sistema"""

    parser = argparse.ArgumentParser(
        prog="market-analyze",
        description="Sistema de Análise de Mercado Financeiro"
    )
    parser.add_argument("--symbol", default="BTC-USD", help="Símbolo do ativo")
    parser.add_argument("--period", default="1y", help="Período de dados")
    parser.add_argument("--interval", default="1d", help="Intervalo dos dados")
    parser.add_argument("--example", choices=['basic', 'strategy'], help="Executar exemplo")
    parser.add_argument("--plot", action="store_true", help="Mostrar gráficos")

    args = parser.parse_args()

    if args.example == 'basic':
        run_basic_example(args)
    elif args.example == 'strategy':
        run_strategy_example(args)
    else:
        run_simple_analysis(args)


def run_simple_analysis(args) -> None:
    """Análise simples do ativo"""

    print(f"=== Análise de {args.symbol} ===")

    # Criar asset
    provider = YahooProvider(period=args.period, interval=args.interval)
    asset = Crypto(args.symbol, provider=provider)

    # Obter dados básicos
    current_price = asset.get_current_price()
    df = asset.get_prices()

    print(f"Preço Atual: ${float(current_price):.2f}")
    print(f"Período: {args.period}")
    print(f"Intervalo: {args.interval}")
    print(f"Número de registros: {len(df)}")

    # Calcular indicadores básicos
    sma_20 = SimpleMovingAverage(period=20)
    rsi = Rsi(period=14)
    macd = Macd()
    stoch = StochRsi()
    sharpe = SharpeRatio()
    sortino = SortinoRatio()

    sma_value = sma_20.calculate(asset).iloc[-1]
    rsi_value = rsi.calculate(asset).iloc[-1]
    macd_value = macd.calculate(asset)['macd'].iloc[-1]
    try:
        stoch_result = stoch.calculate(asset)
        stoch_value = stoch_result['d'].iloc[-1] if len(stoch_result) > 0 else 0.0
    except:
        stoch_value = 0.0

    try:
        sharpe_result = sharpe.calculate(asset)
        sharpe_value = sharpe_result.iloc[-1] if len(sharpe_result) > 0 and not pd.isna(sharpe_result.iloc[-1]) else 0.0
    except:
        sharpe_value = 0.0

    try:
        sortino_result = sortino.calculate(asset)
        sortino_value = sortino_result.iloc[-1] if len(sortino_result) > 0 and not pd.isna(sortino_result.iloc[-1]) else 0.0
    except:
        sortino_value = 0.0

    print(f"\n=== Indicadores ===")
    print(f"SMA 20: ${sma_value:.2f}")
    print(f"RSI 14: {rsi_value:.2f}")
    print(f"MACD: {macd_value:.4f}")
    print(f"Stochastic: {stoch_value:.2f}")
    print(f"Sharpe: {sharpe_value:.2f}")
    print(f"Sortino: {sortino_value:.2f}")

    # Gerar sinais
    rsi_signal = RsiSignal(rsi=rsi)
    macd_signal = MacdSignal(macd=macd)
    stoch_signal = StochRsiSignal(stoch=stoch)
    sharpe_signal = SharpeSignal(sharpe=sharpe)
    sortino_signal = SortinoSignal(sortino=sortino)

    rsi_signals = rsi_signal.generate_signals(asset)
    macd_signals = macd_signal.generate_signals(asset)
    stoch_signals = stoch_signal.generate_signals(asset)
    sharpe_signals = sharpe_signal.generate_signals(asset)
    sortino_signals = sortino_signal.generate_signals(asset)

    # Sinal combinado
    combined = CombinedSignal(
        signals=[rsi_signal, stoch_signal, sharpe_signal, sortino_signal],
        weights=[1.0, 1.0, 1.0, 1.0],
        quantity_threshold=3.0
    )
    combined_signals = combined.generate_signals(asset)

    comfirmed = CombinedSignal(
        signals=[sharpe_signal, sortino_signal],
        weights=[1.0, 1.0],
        quantity_threshold=2.0
    )
    comfirmed_signals = comfirmed.confirm_signals(asset)

    # Contar sinais
    rsi_buy = (rsi_signals == -1).sum()
    rsi_sell = (rsi_signals == 1).sum()
    macd_buy = (macd_signals == 1).sum()
    macd_sell = (macd_signals == -1).sum()
    stoch_buy = (stoch_signals == -1).sum()
    stoch_sell = (stoch_signals == 1).sum()
    sharpe_buy = (sharpe_signals == -1).sum()
    sharpe_sell = (sharpe_signals == 1).sum()
    sortino_buy = (sortino_signals == -1).sum()
    sortino_sell = (sortino_signals == 1).sum()
    combined_buy = (combined_signals == -1).sum()
    combined_sell = (combined_signals == 1).sum()
    confirmed_buy = (comfirmed_signals == -1).sum()
    confirmed_sell = (comfirmed_signals == 1).sum()

    print(f"\n=== Sinais ===")
    print(f"RSI - Compras: {rsi_buy}, Vendas: {rsi_sell}")
    print(f"MACD - Compras: {macd_buy}, Vendas: {macd_sell}")
    print(f"Stochastic - Compras: {stoch_buy}, Vendas: {stoch_sell}")
    print(f"Sharpe - Compras: {sharpe_buy}, Vendas: {sharpe_sell}")
    print(f"Sortino - Compras: {sortino_buy}, Vendas: {sortino_sell}")
    print(f"Combinado - Compras: {combined_buy}, Vendas: {combined_sell}")
    print(f"Confirmado - Compras: {confirmed_buy}, Vendas: {confirmed_sell}")

    # Último sinal
    last_signal = combined_signals.iloc[-1]
    if last_signal == -1:
        print("Último sinal: COMPRA")
    elif last_signal == 1:
        print("Último sinal: VENDA")
    else:
        print("Último sinal: NEUTRO")

    # Plotar se solicitado
    if args.plot:
        print("\nGerando gráfico...")
        ChartPlotter.plot_candlestick_with_signals(
            df=df,
            title=f"{args.symbol} - Análise Técnica",
            buy_signals=combined_signals == -1,
            sell_signals=combined_signals == 1,
            show_volume=True
        )

        ChartPlotter.plot_candlestick_with_signals(
            df=df,
            title=f"{args.symbol} - Análise Técnica (Confirmado)",
            buy_signals=comfirmed_signals == -1,
            sell_signals=comfirmed_signals == 1,
            show_volume=True
        )


def run_basic_example(args) -> None:
    """Executar exemplo básico"""
    from market_analyze.examples.basic_usage import main as basic_main
    basic_main()


def run_strategy_example(args) -> None:
    """Executar exemplo de estratégia"""
    from market_analyze.examples.strategy_analysis import analyze_btc_strategy
    analyze_btc_strategy()


if __name__ == "__main__":
    main()
