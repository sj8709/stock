# services/ticker_manager.py
from services.data_access.ticker_mapper import insert_ticker, select_all_tickers

def add_ticker(ticker: str, name: str, market: str):
    """
    티커 정보를 stock_ticker 테이블에 저장한다.
    이미 존재하면 무시됨 (UNIQUE 제약으로 중복 방지)
    """
    insert_ticker(ticker, name, market)

def get_all_tickers():
    """
    저장된 모든 티커 정보를 조회한다.

    Returns:
        List[dict]: 티커, 이름, 시장 정보 리스트
    """
    return select_all_tickers()
