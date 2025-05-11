import pandas as pd

def calculate_bollinger_bands(close: pd.Series, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    """
    볼린저 밴드 계산

    Parameters:
        close (pd.Series): 종가 시리즈
        window (int): 이동 평균 기간 (기본 20)
        num_std (float): 표준편차 배수 (기본 2.0)

    Returns:
        pd.DataFrame: [upper, middle, lower] 컬럼 포함
    """
    middle_band = close.rolling(window=window).mean()
    std = close.rolling(window=window).std()
    upper_band = middle_band + num_std * std
    lower_band = middle_band - num_std * std

    return pd.DataFrame({
        'upper': upper_band,
        'middle': middle_band,
        'lower': lower_band
    })