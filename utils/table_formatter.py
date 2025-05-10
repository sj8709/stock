import unicodedata

def get_display_width(text):
    """한글 등 전각 문자는 2칸으로 계산"""
    width = 0
    for ch in str(text):
        if unicodedata.east_asian_width(ch) in ('F', 'W', 'A'):
            width += 2
        else:
            width += 1
    return width

def pad_text(text, target_width):
    """표시 너비 기준으로 오른쪽 공백을 추가해 정렬"""
    padding = target_width - get_display_width(text)
    return str(text) + ' ' * max(padding, 0)

def print_table(data, headers):
    col_widths = {h: get_display_width(h) for h in headers}
    for row in data:
        for h in headers:
            col_widths[h] = max(col_widths[h], get_display_width(row[h]))

    header_line = " | ".join(f"{h:<{col_widths[h]}}" for h in headers)
    print(header_line)
    print("-" * get_display_width(header_line))

    for row in data:
        row_line = " | ".join(f"{str(row[h]):<{col_widths[h]}}" for h in headers)
        print(row_line)
