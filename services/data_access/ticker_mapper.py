# services/data_access/ticker_mapper.py
from db.mysql_connector import get_connection

def select_all_tickers() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ticker, name, market
        FROM stock_ticker
        ORDER BY ticker
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def insert_ticker(ticker: str, name: str, market: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO stock_ticker (ticker, name, market)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE name = VALUES(name), market = VALUES(market)
    """, (ticker, name, market))
    conn.commit()
    cursor.close()
    conn.close()