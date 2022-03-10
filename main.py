"""
The main script that runs them all
"""
import numpy as np
import pandas as pd

from json2pd import main_json2pd
from sentiment_analysis import main_sentiment_analysis
from stock_data import main_stock_data
from twitter_api_call import main_twitter_api_call


def quick_pandas():
    file = pd.read_csv("finished_worksheet.csv")
    file_mod = file[abs(file["percentage_change"]) > 2]
    file_length = len(file_mod)
    negative_increase = file_mod[
        (file_mod["classification"] == 0) & (file_mod["label"] == 1)
    ]
    negative_decrease = file_mod[
        (file_mod["classification"] == 0) & (file_mod["label"] == 0)
    ]
    positive_increase = file_mod[
        (file_mod["classification"] == 1) & (file_mod["label"] == 1)
    ]
    positive_decrease = file_mod[
        (file_mod["classification"] == 1) & (file_mod["label"] == 0)
    ]
    print("negative_increase")
    print(len(negative_increase) / file_length)
    print("negative_decrease")
    print(len(negative_decrease) / file_length)
    print("positive_increase")
    print(len(positive_increase) / file_length)
    print("positive_decrease")
    print(len(positive_decrease) / file_length)


if __name__ == "__main__":
    price = "close"
    main_twitter_api_call("2022-03-06T00:00:00.000Z")

    df_twitter = main_json2pd("")

    df_stock = main_stock_data("TSLA", "2022-01-01")

    df = pd.merge(df_twitter, df_stock, on=["date"], how="left")

    df = df[["date", "percentage_change", "text"]]
    df["classification"] = main_sentiment_analysis(df["text"].to_list())
    df["label"] = [1 if x > 0 else 0 for x in df["percentage_change"]]
