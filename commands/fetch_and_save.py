#commands/fetch_and_save.py
from services.ticker_manager import get_all_tickers
from services.fetcher import fetch_stock_data
from services.inserter import insert_daily_price
from datetime import datetime

def parse_date_input(date_str: str) -> str:
    try:
        if date_str.isdigit() and len(date_str) == 8:
            return datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError(f"❌ 잘못된 날짜 형식입니다: {date_str}")

def fetch_and_save_flow():
    try:
        start_raw = input("시작일 (예: 2025-01-01 또는 20250101): ").strip()
        end_raw = input("종료일 (예: 2025-04-30 또는 20250430): ").strip()

        start_str = parse_date_input(start_raw)
        end_str = parse_date_input(end_raw)

        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d")

        if end_date <= start_date:
            print("❌ 종료일은 시작일보다 같거나 이전일 수 없습니다.")
            return

        if (end_date - start_date).days > 365:
            print("❌ 시작일과 종료일의 간격은 최대 365일까지만 허용됩니다.")
            return

    except ValueError as ve:
        print(ve)
        return

    tickers = get_all_tickers()
    if not tickers:
        print("❗ 등록된 티커가 없습니다.")
        return

    for t in tickers:
        ticker = t['ticker']
        name = t['name']
        print(f"\n[▶] {ticker} ({name}) 수집 중...")

        try:
            df = fetch_stock_data(ticker, start_date, end_date)

            print(f"[🧪] {ticker} 수집된 행 수: {len(df)}")

            if df.empty:
                print(f"[✗] {ticker}: 수집된 데이터가 없습니다.")
                continue

            insert_daily_price(df, ticker)
            print(f"[✓] {ticker} 저장 완료")

        except Exception as e:
            print(f"[✗] {ticker} 저장 실패: {e}")

if __name__ == "__main__":
    fetch_and_save_flow()
