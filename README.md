# stock_sentiment_analysis

Using TSLA tweets to earn serious alpha. **Currently under development**

## Background
The aim of this repository is to develop a set of python scripts to scrape and analyse public sentiment about a specified stock/crypocurrency, and see if this has any predictive power when considering short term increases in price. Specifically, this repo is currently restricted to:
- One ticker only (TSLA - Tesla); functionality for other tickers will be included in future commits.
- Sentiment scraped from tweets, categorised as: 'positive', 'negative' and 'neutral'.
- Changes in price on a daily scale (other time-frames *may* be investigated in the future).

## The Approach
1. The daily stock prices are scraped from yahoo finance using the `yfinance` library, this allows a comparison between daily prices and see if there is any gap-up/down behaviours between the last day's closing price and the current day's open price. See 'stock_data.py'.
2. Tweets are gathered that mention the ticker (i.e. TSLA for Tesla), this was chosen over using the full name since it is more likely that active investors and traders use this language. This is performed in the `twitter_api_call.py` script, which can be run by the function `main_twitter_api_call`.
3. The tweets scraped in step 2 are grouped into 'positive', 'negative' and 'neutral'. This is performed by the `sentiment-roberta-large-english` model with the script `sentiment_analysis.py`.
4. Perform simple correlation tests to identify if the overall twitter sentiment has any predictive power on the daily price movements.

## WIP
The current aim is to finalise:
1. The data collection, as twitter's basic API only allows access to the last weeks worth of data.
2. The analysis of the current approach.

## Future work
Currently, this repository is in a very basic state. In the future I plan to work on (not in any order):
1. Expanding the number of stocks or crypocurrencys used.
2. Increasing the historic data range of tweets.
3. Gathering sentiment data from multiple sources (e.g. reddit, comments on financal websites).
4. Fine-tune the sentiment analysis model.
