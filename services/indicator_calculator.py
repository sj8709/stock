# services/indicator_calculator.py
import pandas as pd
from services.data_access.indicator_mapper import insert_indicator
from services.data_access.price_mapper import get_price_dataframe
from services.indicators.rsi import calculate_rsi
from services.indicators.macd import calculate_macd
from services.indicators.bollinger import calculate_bollinger_bands
from services.indicators.ichimoku import calculate_ichimoku

def calculate_and_store_indicators(ticker: str):
    df = get_price_dataframe(ticker)

    # RSI
    rsi = calculate_rsi(df['close_price'])
    for date, value in rsi.dropna().items():
        insert_indicator(ticker, date, 'rsi', 'rsi_14', value)

    # MACD
    macd_df = calculate_macd(df['close_price'])
    for col in macd_df.columns:
        for date, value in macd_df[col].dropna().items():
            insert_indicator(ticker, date, 'macd', col, value)

    # Bollinger Bands
    bb_df = calculate_bollinger_bands(df['close_price'])
    for col in bb_df.columns:
        for date, value in bb_df[col].dropna().items():
            insert_indicator(ticker, date, 'bollinger', col, value)

    # Ichimoku
    ichi_df = calculate_ichimoku(df['high_price'], df['low_price'], df['close_price'])
    for col in ichi_df.columns:
        for date, value in ichi_df[col].dropna().items():
            insert_indicator(ticker, date, 'ichimoku', col, value)
