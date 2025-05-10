import unicodedata
from db.mysql_connector import get_connection

def get_display_width(text):
    width = 0
    for ch in str(text):
        if unicodedata.east_asian_width(ch) in ('F', 'W', 'A'):
            width += 2
        else:
            width += 1
    return width

def print_table(data, headers):
    col_widths = {h: get_display_width(h) for h in headers}
    for row in data:
        for h in headers:
            col_widths[h] = max(col_widths[h], get_display_width(row[h]))

    header_line = " | ".join(f"{h:<{col_widths[h]}}" for h in headers)
    print(header_line)
    print("-" * get_display_width(header_line))

    for row in data:
        row_line = " | ".join(f"{str(row[h]):<{col_widths[h]}}" for h in headers)
        print(row_line)

def view_prices_list():
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
