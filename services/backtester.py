# service/backtester.py
from db.mysql_connector import get_connection
from commands.analyze_returns import calculate_returns, fit_maxwell_distribution, find_outliers


def get_price_and_dates(ticker: str) -> list[dict]:
    """
    티커의 날짜별 open/close 데이터 조회 (오름차순)
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT trade_date, open_price, close_price
        FROM daily_price
        WHERE ticker = %s
        ORDER BY trade_date ASC
    """
    cursor.execute(query, (ticker,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def run_maxwell_backtest(ticker: str, hold_days: int = 5, 
                        take_profit: float = 0.05, stop_loss: float = -0.03):
    """
    맥스웰 하단 이상치 발생 다음 날 매수 → 익절/손절/최대 보유일 조건으로 청산
    """
    price_data = get_price_and_dates(ticker)
    dates = [row['trade_date'] for row in price_data]
    closes = [row['close_price'] for row in price_data]

    returns = calculate_returns(closes)
    maxwell_bounds = fit_maxwell_distribution(returns)
    outliers = find_outliers(returns, dates, maxwell_bounds)

    trades = []

    for date, _ in outliers:
        if date not in dates:
            continue
        idx = dates.index(date)
        entry_idx = idx + 1
        if entry_idx >= len(price_data):
            continue

        entry_open = price_data[entry_idx]['open_price']
        entry_date = dates[entry_idx]
        exit_date = None
        exit_price = None
        result = None

        for offset in range(hold_days):
            check_idx = entry_idx + offset
            if check_idx >= len(price_data):
                break
            today_close = price_data[check_idx]['close_price']
            daily_return = (today_close - entry_open) / entry_open

            if daily_return >= take_profit:
                exit_date = dates[check_idx]
                exit_price = today_close
                result = '익절'
                break
            elif daily_return <= stop_loss:
                exit_date = dates[check_idx]
                exit_price = today_close
                result = '손절'
                break

        if not exit_date:
            # 최대 보유일 도달
            final_idx = min(entry_idx + hold_days, len(price_data) - 1)
            exit_date = dates[final_idx]
            exit_price = price_data[final_idx]['close_price']
            result = '기간만료'

        profit = (exit_price - entry_open) / entry_open
        trades.append({
            'entry_date': entry_date,
            'exit_date': exit_date,
            'entry_price': entry_open,
            'exit_price': exit_price,
            'return': profit,
            'result': result
        })

    return trades
