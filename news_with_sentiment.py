from GoogleNews import GoogleNews
import newspaper
import pandas as pd
import json

from transformers import pipeline
from GoogleNews import GoogleNews
import newspaper
import pandas as pd
import datetime

def fetch_news(company, lang='en', end_date=None):
    googlenews = GoogleNews(lang=lang)
    googlenews.search(company)

    all_results = []
    seen_links = set()
    unique_results = []

    page = 1
    keep_scraping = True

    if isinstance(end_date, str):
        end_date = datetime.datetime.fromisoformat(end_date)
    elif end_date is None:
        end_date = datetime.datetime.min  # Effectively no end

    while keep_scraping:
        googlenews.getpage(page)
        results = googlenews.results()

        if not results:
            break  # No more results

        for article in results:
            # Clean link
            clean_link = article['link'].split('&ved=')[0]
            if clean_link in seen_links:
                continue

            # Parse article date
            pub_date = article.get('datetime')
            if not pub_date:
                continue  # Skip if no date

            if pub_date < end_date:
                keep_scraping = False
                break  # Stop if any article is older than end_date

            seen_links.add(clean_link)
            article['link'] = clean_link
            unique_results.append(article)

        page += 1

    print(f"Found {len(unique_results)} unique articles.")
    print(f"Scraped unti page {page}")

    final_df = pd.DataFrame(columns=['date', 'source', 'title', 'description', 'link'])
    for a in unique_results:
        try:
            article = newspaper.Article(a['link'])
            article.download()
            article.parse()
            final_df = pd.concat([final_df, pd.DataFrame([{
                'date': a['datetime'].isoformat(),
                'source': a['media'],
                'title': article.title,
                'description': article.summary,
                'content': article.text,
                'link': a['link']
            }])], ignore_index=True)
        except Exception as e:
            print(f"Error downloading/parsing article: {e}")
            continue

    return final_df


def analyze_sentiment(news_df,to_json=False):
    sentiment_pipeline = pipeline("sentiment-analysis")

    results = []
    for _, row in news_df.iterrows():
        text = f"{row['title']} {row['content'] or ''}"
        sentiment = sentiment_pipeline(text[:512])[0]  # Truncate to 512 tokens
        article = row.to_dict()
        article['sentiment'] = sentiment
        results.append(article)

    if to_json:
        with open("apple_news_with_sentiment.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"Saved {len(results)} articles with sentiment to apple_news_with_sentiment.json")

    return results
