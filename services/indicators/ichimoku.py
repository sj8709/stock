# services/indicators/ichimoku.py
import pandas as pd

def calculate_ichimoku(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.DataFrame:
    """
    일목균형표 구성 요소 계산

    Parameters:
        high (pd.Series): 고가 시리즈
        low (pd.Series): 저가 시리즈
        close (pd.Series): 종가 시리즈

    Returns:
        pd.DataFrame: conversion_line, base_line, leading_span_a, leading_span_b, lagging_span 포함
    """
    # 전환선 (9일 최고/최저 평균)
    conversion_line = (high.rolling(window=9).max() + low.rolling(window=9).min()) / 2

    # 기준선 (26일 최고/최저 평균)
    base_line = (high.rolling(window=26).max() + low.rolling(window=26).min()) / 2

    # 선행스팬1: (전환선 + 기준선) / 2 → 26일 앞당김
    leading_span_a = ((conversion_line + base_line) / 2).shift(26)

    # 선행스팬2: 52일 최고/최저 평균 → 26일 앞당김
    leading_span_b = ((high.rolling(window=52).max() + low.rolling(window=52).min()) / 2).shift(26)

    # 후행스팬: 종가를 26일 뒤로 이동
    lagging_span = close.shift(-26)

    return pd.DataFrame({
        'conversion_line': conversion_line,
        'base_line': base_line,
        'leading_span_a': leading_span_a,
        'leading_span_b': leading_span_b,
        'lagging_span': lagging_span
    })
