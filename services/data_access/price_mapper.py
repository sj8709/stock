from db.mysql_connector import get_connection

def select_price_table(ticker: str, limit: int = 50) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, ticker, trade_date, open_price, high_price, low_price, close_price, volume
        FROM daily_price
        WHERE ticker = %s
        ORDER BY trade_date DESC
        LIMIT %s
    """, (ticker, limit))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def select_recent_prices_by_ticker(ticker: str, limit: int = 50) -> list[dict]:
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
    LIMIT %s
    """
    cursor.execute(query, (ticker, limit))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def select_recent_close_prices_with_date(ticker: str, limit: int = 60) -> list[tuple]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT trade_date, close_price
        FROM daily_price
        WHERE ticker = %s
        ORDER BY trade_date DESC
        LIMIT %s
    """, (ticker, limit))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return sorted(rows, key=lambda x: x[0])  # 오름차순 정렬

def insert_daily_price_record(ticker, trade_date, open_price, high_price, low_price, close_price, volume):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO daily_price (
            ticker, trade_date, open_price, high_price,
            low_price, close_price, volume
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            open_price = VALUES(open_price),
            high_price = VALUES(high_price),
            low_price = VALUES(low_price),
            close_price = VALUES(close_price),
            volume = VALUES(volume)
    """, (ticker, trade_date, open_price, high_price, low_price, close_price, volume))

    conn.commit()
    cursor.close()
    conn.close()