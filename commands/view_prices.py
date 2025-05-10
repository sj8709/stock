# view_prices.py
from services.data_access.price_mapper import select_recent_prices_by_ticker
from utils.table_formatter import print_table

def view_prices_list():
    """특정 티커의 최근 50개 일별 주가를 출력하는 함수"""
    ticker = input("조회할 티커를 입력하세요 (예: AAPL): ").strip().upper()
    if not ticker:
        print("❗ 티커를 입력하지 않았습니다.")
        return

    rows = select_recent_prices_by_ticker(ticker)

    if rows:
        headers = list(rows[0].keys())
        print_table(rows, headers)
    else:
        print(f"📭 '{ticker}'에 대한 가격 데이터가 없습니다.")

if __name__ == "__main__":
    view_prices_list()
