"""
The main script that runs them all
"""
import numpy as np
import pandas as pd

from json2pd import main_json2pd
from sentiment_analysis import main_sentiment_analysis
from stock_data import main_stock_data
from twitter_api_call import main_twitter_api_call
from helper import date_to_download

if __name__ == "__main__":
    price="close"    
    
    dates=date_to_download()
    
    main_twitter_api_call(dates)
    
    df_twitter=main_json2pd("")
    
    df_twitter.to_csv("twitter_data.csv",index=False)
    
    df_stock=main_stock_data("TSLA","2022-01-01")
    
    df=pd.merge(df_twitter,df_stock,on=["date"],how="left")

    df=df[["date","percentage_change","text"]]
    df["classification"]=main_sentiment_analysis(df["text"].to_list())
    df["label"]=[1 if x>0 else 0 for x in df["percentage_change"]]
    
    df.to_csv("labeled_classified_tweets.csv",index=False)
    
    

