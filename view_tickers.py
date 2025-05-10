import unicodedata
from services.ticker_manager import get_all_tickers

def get_display_width(text):
    """한글 등 전각 문자는 2칸으로 계산"""
    width = 0
    for ch in str(text):
        if unicodedata.east_asian_width(ch) in ['F', 'W']:  # 전각, 넓은 문자
            width += 2
        else:
            width += 1
    return width

def pad_text(text, target_width):
    """실제 표시 너비 기준으로 오른쪽 공백 추가"""
    padding = target_width - get_display_width(text)
    return str(text) + ' ' * padding

def print_ticker_table(tickers):
    print("\n📄 등록된 티커 목록\n")

    headers = ["Ticker", "Name", "Market"]
    col_widths = [10, 20, 10]

    # 헤더 출력
    header_row = ' | '.join(pad_text(h, w) for h, w in zip(headers, col_widths))
    print(header_row)
    print('-' * len(header_row))

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
