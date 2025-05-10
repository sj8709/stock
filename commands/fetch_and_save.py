from services.ticker_manager import get_all_tickers
from services.fetcher import fetch_stock_data
from services.inserter import insert_daily_price

def fetch_and_save_flow():
    start = input("시작일 (예: 2025-01-01): ").strip()
    end = input("종료일 (예: 2025-04-30): ").strip()

    tickers = get_all_tickers()
    if not tickers:
        print("❗ 등록된 티커가 없습니다.")
        return

    for t in tickers:
        print(f"\n[▶] {t['ticker']} ({t['name']}) 수집 중...")
        df = fetch_stock_data(t['ticker'], start, end)
        insert_daily_price(df, t['ticker'])
        print(f"[✓] {t['ticker']} 저장 완료")

if __name__ == "__main__":
    fetch_and_save_flow()
