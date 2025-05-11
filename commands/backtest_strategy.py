#commands/backtest_strategy.py
from services.backtester import run_maxwell_backtest

def backtest_cli():
    ticker = input("티커를 입력하세요: ").strip().upper()
    hold_days = int(input("최대 보유 일수 (예: 5): ").strip())
    take_profit = float(input("익절 기준 수익률 (예: 0.05): ").strip())
    stop_loss = float(input("손절 기준 수익률 (예: -0.03): ").strip())

    trades = run_maxwell_backtest(
        ticker, hold_days=hold_days, take_profit=take_profit, stop_loss=stop_loss
    )

    if not trades:
        print("⚠️ 테스트 가능한 매매가 없습니다.")
        return

    print(f"\n📊 백테스트 결과 ({len(trades)}회 거래):")
    total = 0
    win = 0

    for t in trades:
        r = t['return']
        total += r
        if r > 0:
            win += 1
        print(f"{t['entry_date']} → {t['exit_date']} | {t['result']:4}: {r:.2%}")

    avg_return = total / len(trades)
    win_rate = win / len(trades)

    print(f"\n📈 평균 수익률: {avg_return:.2%}")
    print(f"✅ 승률: {win_rate:.2%}")

if __name__ == "__main__":
    backtest_cli()
