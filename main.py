from services.fetcher import fetch_stock_data
from services.inserter import insert_daily_price

ticker = 'NVDA'
df = fetch_stock_data(ticker, '2025-01-01', '2025-04-30')
insert_daily_price(df, ticker)

print(f"{len(df)}건의 주가 데이터를 '{ticker}'로 저장했습니다.")
