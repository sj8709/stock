from db.mysql_connector import get_connection
import datetime

def add_ticker(ticker: str, name: str, market: str):
    """
    티커 정보를 stock_ticker 테이블에 저장한다.
    이미 존재하면 무시됨 (UNIQUE 제약으로 중복 방지)

    Parameters:
        ticker (str): 종목코드
        name (str): 종목명
        market (str): 시장구분 (NASDAQ, KOSPI 등)
    """
    conn = get_connection()
    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO stock_ticker (ticker, name, market, created_at)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            market = VALUES(market)
    """

    cursor.execute(insert_sql, (
        ticker,
        name,
        market,
        datetime.datetime.now()
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_all_tickers():
    """
    저장된 모든 티커 정보를 조회한다.

    Returns:
        List[dict]: 티커, 이름, 시장 정보 리스트
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT ticker, name, market FROM stock_ticker ORDER BY ticker")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows
