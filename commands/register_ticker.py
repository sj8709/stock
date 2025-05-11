#commands/register_ticker.py
from services.ticker_manager import add_ticker

def register_ticker_flow():
    while True:
        ticker = input("종목코드 입력 (예: NVDA, 005930.KS) (Enter로 종료): ").strip()
        if ticker == '':
            break
        name = input("종목명 (예: 엔비디아): ").strip()
        market = input("시장 (예: NASDAQ, KOSPI): ").strip()
        add_ticker(ticker, name, market)
        print(f"[+] {ticker} 등록 완료\n")

if __name__ == "__main__":
    register_ticker_flow()
