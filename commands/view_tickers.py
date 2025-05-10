from services.ticker_manager import get_all_tickers
from utils.table_formatter import get_display_width, pad_text

def print_ticker_table(tickers):
    print("\n📄 등록된 티커 목록\n")

    headers = ["Ticker", "Name", "Market"]
    col_widths = [10, 20, 10]

    # 헤더 출력
    header_row = ' | '.join(pad_text(h, w) for h, w in zip(headers, col_widths))
    print(header_row)
    print('-' * get_display_width(header_row))

    # 데이터 출력
    for t in tickers:
        row = [
            pad_text(t['ticker'], col_widths[0]),
            pad_text(t['name'], col_widths[1]),
            pad_text(t['market'], col_widths[2]),
        ]
        print(' | '.join(row))

    print(f"\n총 {len(tickers)}개 티커 등록됨.\n")

def view_ticker_list():
    tickers = get_all_tickers()
    if not tickers:
        print("❗ 등록된 티커가 없습니다.")
        return

    print_ticker_table(tickers)

if __name__ == "__main__":
    view_ticker_list()
