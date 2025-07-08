import pandas as pd
import matplotlib.pyplot as plt
import json
from stock_fetcher import fetch_tiingo_stock
from news_with_sentiment import fetch_news,analyze_sentiment
from datetime import datetime
import os
from dotenv import load_dotenv  # Add this import

# --- Load API Key from .env ---
load_dotenv()
TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")

TICKER = "AAPL"
COMPANY_NAME = "Apple Inc"
START_DATE = "2024-07-07"
END_DATE = "2025-07-07"
# SENTIMENT_FILE = "apple_news_with_sentiment.json"

# --- Step 1: Load stock data ---
stock_df = fetch_tiingo_stock(TICKER, START_DATE, END_DATE, TIINGO_API_KEY)
stock_df['date'] = pd.to_datetime(stock_df['date']).dt.date
stock_df['return'] = stock_df['adjClose'].pct_change()

# --- Step 2: Load sentiment data ---
news_df = fetch_news(COMPANY_NAME,end_date=START_DATE)
print('fetched news')
results = analyze_sentiment(news_df, to_json=True)
sentiment_df = pd.DataFrame(results)
sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.date

def label_to_score(label):
    return 1 if label == 'POSITIVE' else -1

sentiment_df['score'] = sentiment_df['sentiment'].apply(lambda s: label_to_score(s['label']))
# print(sentiment_dlf)


# Average sentiment score per day
daily_sentiment = sentiment_df.groupby('date', as_index=False)['score'].mean()
# print(daily_sentiment)
# --- Step 3: Merge ---
merged_df = pd.merge(stock_df, daily_sentiment, on='date', how='inner')
print(merged_df)
# --- Step 4: Visualize ---
fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.set_xlabel('Date')
ax1.set_ylabel('Adj Close Price', color='blue')
ax1.plot(merged_df['date'], merged_df['adjClose'], color='blue', label='Stock Price')
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Sentiment Score', color='red')
ax2.plot(merged_df['date'], merged_df['score'], color='red', linestyle='--', label='Sentiment Score')
ax2.tick_params(axis='y', labelcolor='red')

plt.title(f'{TICKER} Stock Price vs News Sentiment')
fig.tight_layout()
plt.show()

# --- Step 5: Correlation ---
correlation = merged_df[['return', 'score']].corr().iloc[0, 1]
print(f"\n📊 Correlation between daily return and sentiment: {correlation:.2f}")
