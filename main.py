from commands.register_ticker import register_ticker_flow
from commands.fetch_and_save import fetch_and_save_flow
from commands.view_tickers import view_ticker_list
from commands.view_prices import view_prices_list
from commands.analyze_returns import run_return_analysis
from commands.backtest_strategy import backtest_cli

def main():
    while True:
        print("\n🟢 Stock Manager")
        print("1. 티커 등록")
        print("2. 주가 수집 및 저장")
        print("3. 등록된 티커 보기")
        print("4. 주가 데이터 조회")
        print("5. 수익률 분석")
        print("6. 백테스트 실행")
        print("0. 종료")
        choice = input("선택 (0~6): ").strip()

        if choice == '1':
            register_ticker_flow()
        elif choice == '2':
            fetch_and_save_flow()
        elif choice == '3':
            view_ticker_list()
        elif choice == '4':
            view_prices_list()
        elif choice == '5':
            run_return_analysis()
        elif choice == '6':
            backtest_cli()
        elif choice == '0':
            print("👋 프로그램을 종료합니다.")
            break
        else:
            print("❗ 잘못된 선택입니다.")

if __name__ == "__main__":
    main()
