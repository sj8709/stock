from db.mysql_connector import get_connection
from utils.table_formatter import print_table  # ✅ 공통 유틸에서 가져옴

def view_prices_list():
    """특정 티커의 최근 50개 일별 주가를 출력하는 함수"""
    ticker = input("조회할 티커를 입력하세요 (예: AAPL): ").strip().upper()
    if not ticker:
        print("❗ 티커를 입력하지 않았습니다.")
        return

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        CAST(@rownum := @rownum + 1 AS UNSIGNED) AS rownum,
        ticker,
        trade_date,
        open_price,
        high_price,
        low_price,
        close_price,
        volume
    FROM daily_price,
        (SELECT @rownum := 0) AS r
    WHERE ticker = %s
    ORDER BY trade_date DESC
    LIMIT 50
    """
    cursor.execute(query, (ticker,))
    rows = cursor.fetchall()

    if rows:
        headers = list(rows[0].keys())
        print_table(rows, headers)
    else:
        print(f"📭 '{ticker}'에 대한 가격 데이터가 없습니다.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    view_prices_list()
