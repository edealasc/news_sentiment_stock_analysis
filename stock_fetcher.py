from tiingo import TiingoClient
import pandas as pd

def fetch_tiingo_stock(ticker, start_date, end_date, api_key):
    config = {'api_key': api_key}
    client = TiingoClient(config)

    df = client.get_dataframe(ticker,
                              startDate=start_date,
                              endDate=end_date,
                              frequency='daily')

    # Reset index so the date becomes a column
    df.reset_index(inplace=True)

    # Save to CSV
    filename = f"{ticker}_stock_data_{start_date}_to_{end_date}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Stock data saved to {filename}")

    return df

if __name__ == "__main__":
    API_KEY = "11664da9a3e3dfd3fe0132eabd107242f57790b8"
    ticker = "AAPL"
    start_date = "2025-06-01"
    end_date = "2025-07-01"

    fetch_tiingo_stock(ticker, start_date, end_date, API_KEY)
