# services/analyzer.py

import numpy as np
from scipy.stats import maxwell

def calculate_returns(prices: list[float]) -> list[float]:
    """
    주어진 종가 리스트로부터 수익률 리스트를 계산
    :param prices: [100.0, 102.0, 101.0, ...]
    :return: [0.02, -0.0098, ...]
    """
    prices = np.array(prices, dtype=np.float64)
    returns = np.diff(prices) / prices[:-1]
    return returns.tolist()

def fit_maxwell_distribution(returns: list[float]) -> dict:
    """
    수익률 리스트에 대해 맥스웰 분포 피팅 및 경계 계산
    :return: loc, scale, 상/하위 5% 경계값
    """
    # scipy는 입력값이 양수에 가까운 값일수록 좋음
    filtered = [r for r in returns if r > 0]  # ※ 양수만 사용
    if len(filtered) < 5:
        raise ValueError("맥스웰 분포를 피팅할 수익률 데이터가 부족합니다.")

    params = maxwell.fit(filtered)  # loc, scale 추정
    loc, scale = params
    lower = maxwell.ppf(0.05, loc=loc, scale=scale)
    upper = maxwell.ppf(0.95, loc=loc, scale=scale)

    return {
        "loc": loc,
        "scale": scale,
        "lower_bound": lower,
        "upper_bound": upper
    }

def find_outliers(returns: list[float], dates: list, bounds: dict) -> list[tuple]:
    """
    경계 바깥의 이상 수익률을 찾음
    :param returns: 수익률 리스트
    :param dates: trade_date 리스트 (returns[i]는 dates[i+1]에 해당)
    :param bounds: {'lower_bound': ..., 'upper_bound': ...}
    :return: [(날짜, 수익률), ...]
    """
    lower = bounds['lower_bound']
    upper = bounds['upper_bound']
    
    outliers = []
    for i, r in enumerate(returns):
        date = dates[i + 1]
        if r < lower or r > upper:
            outliers.append((date, r))

    return outliers

def fit_normal_distribution(returns: list[float]) -> dict:
    """
    수익률에 대해 정규분포 기반 평균/표준편차를 계산하고 경계값 추정
    """
    arr = np.array(returns)
    mean = np.mean(arr)
    std = np.std(arr)
    lower = mean - 2 * std
    upper = mean + 2 * std

    return {
        "mean": mean,
        "std": std,
        "lower_bound": lower,
        "upper_bound": upper
    }