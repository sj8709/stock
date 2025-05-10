from db.mysql_connector import get_connection
from services.analyzer import (
    calculate_returns,
    fit_maxwell_distribution,
    fit_normal_distribution,
    find_outliers,
)


def get_price_and_dates(ticker: str) -> tuple[list, list]:
    """
    주어진 티커의 최근 60일 종가 및 날짜 조회 (trade_date 오름차순 정렬)
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT trade_date, close_price
    FROM daily_price
    WHERE ticker = %s
    ORDER BY trade_date DESC
    LIMIT 60
    """
    cursor.execute(query, (ticker,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # DESC로 가져왔으므로 날짜 오름차순으로 정렬
    rows.sort(key=lambda x: x[0])
    dates = [row[0] for row in rows]
    prices = [row[1] for row in rows]
    return prices, dates


def run_return_analysis():
    ticker = input("수익률 분석할 티커를 입력하세요: ").strip().upper()
    prices, dates = get_price_and_dates(ticker)

    if len(prices) < 2:
        print("❗ 수익률을 계산할 데이터가 부족합니다.")
        return

    returns = calculate_returns(prices)

    print(f"\n📈 {ticker} 종가 기반 일별 수익률 (최근 60일):")
    for i in range(min(60, len(returns))):
        print(f"{dates[i+1]}: {returns[i]:.4%}")

    # 📊 맥스웰 분포 피팅
    try:
        maxwell_result = fit_maxwell_distribution(returns)
        print("\n📊 맥스웰 분포 분석 결과:")
        print(f" - location (loc)[이동값]: {maxwell_result['loc']:.6f}")
        print(f" - scale[확산도]: {maxwell_result['scale']:.6f}")
        print(f" - 하위 5% 경계: {maxwell_result['lower_bound']:.4%}")
        print(f" - 상위 95% 경계: {maxwell_result['upper_bound']:.4%}")
    except ValueError as ve:
        print(f"\n⚠️ 맥스웰 분포 분석 불가: {ve}")
        maxwell_result = None

    # 📊 정규분포 피팅
    normal_result = fit_normal_distribution(returns)
    print("\n📊 정규분포 분석 결과:")
    print(f" - 평균 (mean): {normal_result['mean']:.4%}")
    print(f" - 표준편차 (std): {normal_result['std']:.4%}")
    print(f" - 하위 경계 (μ - 2σ): {normal_result['lower_bound']:.4%}")
    print(f" - 상위 경계 (μ + 2σ): {normal_result['upper_bound']:.4%}")

    # 🚨 이상 수익률 비교
    print("\n🚨 이상 수익률 비교:")

    if maxwell_result:
        print("맥스웰 기준:")
        mw_outliers = find_outliers(returns, dates, maxwell_result)
        if mw_outliers:
            for date, r in mw_outliers:
                print(f" - {date}: {r:.4%}")
        else:
            print(" - 이상 없음")
    else:
        print("맥스웰 기준: 분석 불가")

    print("정규분포 기준:")
    norm_outliers = find_outliers(returns, dates, normal_result)
    if norm_outliers:
        for date, r in norm_outliers:
            print(f" - {date}: {r:.4%}")
    else:
        print(" - 이상 없음")


if __name__ == "__main__":
    run_return_analysis()
