import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    야후 파이낸스를 통해 주가 데이터를 가져온다.
    
    Parameters:
        ticker (str): 종목코드 (예: '005930.KS')
        start (str): 시작 날짜 (예: '2023-01-01')
        end (str): 종료 날짜 (예: '2023-12-31')
    
    Returns:
        DataFrame: 날짜, 시가, 고가, 저가, 종가, 거래량
    """
    df = yf.download(ticker, start=start, end=end)
    df = df.reset_index()
    
    # ✅ 열 이름 평탄화 (멀티인덱스 제거)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Date'] = pd.to_datetime(df['Date'])
    return df
