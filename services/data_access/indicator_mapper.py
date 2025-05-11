# services/data_access/indicator_mapper.py
from db.mysql_connector import get_connection

def insert_indicator(ticker: str, trade_date, indicator_type: str, line_name: str, value: float):
    """
    기술적 지표 데이터를 technical_indicators 테이블에 저장하거나 갱신
    """
    conn = get_connection()
    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO technical_indicators (
            ticker, trade_date, indicator_type, line_name, value
        ) VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            value = VALUES(value)
    """

    cursor.execute(insert_sql, (ticker, trade_date, indicator_type, line_name, value))
    conn.commit()
    cursor.close()
    conn.close()
