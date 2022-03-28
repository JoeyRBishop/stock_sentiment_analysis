"""
The main script that runs them all
"""
import numpy as np
import pandas as pd

from helper import date_to_download
from json2pd import main_json2pd
from sentiment_analysis import main_sentiment_analysis
from stock_data import main_stock_data
from twitter_api_call import main_twitter_api_call

if __name__ == "__main__":
    price = "close"

    dates = date_to_download()

    main_twitter_api_call(dates)

    df_twitter_current = main_json2pd("", dates)

    df_twitter_master = pd.read_csv("twitter_data.csv")

    new_df_twitter_master = pd.concat([df_twitter_current, df_twitter_master])

    new_df_twitter_master.to_csv("twitter_data.csv", index=False)

    df_stock = main_stock_data("TSLA", "2022-01-01")

    df_current = pd.merge(df_twitter_current, df_stock, on=["date"], how="left")

    df_current = df_current[["date", "percentage_change", "text"]]
    df_current["classification"] = main_sentiment_analysis(df_current["text"].to_list())
    df_current["label"] = [1 if x > 0 else 0 for x in df_current["percentage_change"]]

    df_master = pd.read_csv("labeled_classified_tweets.csv")

    new_df_master = pd.concat([df_current, df_master])

    new_df_master.to_csv("labeled_classified_tweets.csv", index=False)
