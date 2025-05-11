# commands/calc_indicators.py
from services.indicator_calculator import calculate_and_store_indicators

def run_indicator_calc():
    ticker = input("지표를 계산할 티커를 입력하세요 (예: NVDA): ").strip().upper()
    if not ticker:
        print("❗ 티커를 입력하지 않았습니다.")
        return

    try:
        calculate_and_store_indicators(ticker)
        print(f"✅ {ticker} 지표 계산 및 저장 완료")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    run_indicator_calc()
