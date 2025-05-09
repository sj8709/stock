from db.mysql_connector import get_connection
import pandas as pd

def insert_daily_price(df, ticker):
    """
    DataFrame의 주가 데이터를 MySQL 테이블에 삽입한다.

    Parameters:
        df (DataFrame): yfinance로 가져온 주가 데이터
        ticker (str): 종목코드 (예: 'NVDA')
    """
    conn = get_connection()
    cursor = conn.cursor()

    insert_sql = """
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
    """

    for _, row in df.iterrows():
        trade_date = pd.to_datetime(row['Date']).strftime('%Y-%m-%d')  # 강제 변환
        cursor.execute(insert_sql, (
            ticker,
            trade_date,
            float(row['Open']),
            float(row['High']),
            float(row['Low']),
            float(row['Close']),
            int(row['Volume'])
        ))

    conn.commit()
    cursor.close()
    conn.close()
