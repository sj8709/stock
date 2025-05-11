# services/indicators/rsi.py
import pandas as pd

def calculate_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """
    RSI(Relative Strength Index) 계산

    Parameters:
        close (pd.Series): 종가 시리즈
        period (int): RSI 기간 (기본: 14)

    Returns:
        pd.Series: 날짜별 RSI 값 (NaN 포함 가능)
    """
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
