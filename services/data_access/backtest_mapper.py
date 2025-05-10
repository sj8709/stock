from db.mysql_connector import get_connection

def select_all_open_close(ticker: str) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT trade_date, open_price, close_price
        FROM daily_price
        WHERE ticker = %s
        ORDER BY trade_date ASC
    """, (ticker,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows