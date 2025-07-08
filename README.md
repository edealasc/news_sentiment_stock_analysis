# News Sentiment Stock Analysis

This project analyzes the relationship between news sentiment and stock price movements for a given company (e.g., Apple Inc). It scrapes news articles using Google News, performs sentiment analysis with Hugging Face Transformers, and visualizes the correlation with historical stock data.

## Features

- Scrape recent news articles for a company using Google News
- Extract and clean article content with `newspaper3k`
- Perform sentiment analysis on news headlines and content
- Fetch historical stock data from Tiingo
- Visualize stock price and sentiment trends together
- Calculate correlation between daily sentiment and stock returns

## Requirements

- Python 3.8+
- pandas
- matplotlib
- newspaper3k
- GoogleNews
- transformers
- torch

## Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/your-github-username/news-sentiment-stock-analysis.git
    cd news-sentiment-stock-analysis
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set your Tiingo API key in your environment.

4. Run the analysis:
    ```bash
    python main.py
    ```

5. View the output plot and correlation in your terminal.

## Notes

- The project currently supports English news only.
- Sentiment analysis uses a pre-trained Hugging Face pipeline.
- For best results, ensure you have a stable internet connection for scraping and model downloads.
