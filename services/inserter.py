# services/inserter.py
import pandas as pd
from services.data_access.price_mapper import insert_daily_price_record

def insert_daily_price(df, ticker):
    """
    DataFrame의 주가 데이터를 daily_price 테이블에 삽입한다.
    날짜 포맷 오류를 방지하기 위해 Date 컬럼이 없으면 인덱스를 초기화한다.
    """
    # Date 컬럼이 없으면 인덱스를 초기화하여 Date 컬럼 생성
    if 'Date' not in df.columns:
        df = df.reset_index()

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    for _, row in df.iterrows():
        if pd.isnull(row['Date']):
            raise ValueError(f"날짜 파싱 실패: {row['Date']}")

        trade_date = row['Date'].strftime('%Y-%m-%d')

        insert_daily_price_record(
            ticker=ticker,
            trade_date=trade_date,
            open_price=float(row['Open']),
            high_price=float(row['High']),
            low_price=float(row['Low']),
            close_price=float(row['Close']),
            volume=int(row['Volume'])
        )