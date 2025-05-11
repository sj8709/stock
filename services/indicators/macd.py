# services/indicators/macd.py
import pandas as pd

def calculate_macd(close: pd.Series,
                   fast_period: int = 12,
                   slow_period: int = 26,
                   signal_period: int = 9) -> pd.DataFrame:
    """
    MACD 계산

    Parameters:
        close (pd.Series): 종가 시리즈
        fast_period (int): 단기 EMA 기간
        slow_period (int): 장기 EMA 기간
        signal_period (int): Signal EMA 기간

    Returns:
        pd.DataFrame: [macd, signal, histogram] 컬럼 포함
    """
    ema_fast = close.ewm(span=fast_period, adjust=False).mean()
    ema_slow = close.ewm(span=slow_period, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line

    return pd.DataFrame({
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram
    })
