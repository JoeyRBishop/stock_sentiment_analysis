'''
functions required to gather the stock data from yahoo finance
'''
import pandas as pd
import yfinance as yf
import numpy as np

def main_stock_data(tick="TSLA",start_date="2022-01-01"):
    '''
    Get historical stock data from yahoo finance and save it as a csv
    Parameters
    ----------
    tick : str, optional
        The ticker, The default is "TSLA".
    start_date : TYPE, optional
        The initial start data of the histroy. The default is "2022-01-01".

    Returns
    -------
    Saves the historical data as a csv where the file name is defined by the
    most current date
    '''    
    ticker = yf.Ticker(tick)
    df = ticker.history(start=start_date,interval="1d")
    df=df.reset_index()
    
    df["ticker"]=tick
    
    ###A personal preference, to make all the headers lower case
    df.columns = [x.lower() for x in df.columns]

    df=percentage_growth(df)
    
    final_date=str(df["date"].max())[:10]
    df.to_csv(f"stock_data_{tick}_{final_date}.csv",index=False)
    return df



def percentage_growth(df):
    '''
    Assumption that the price is the close price as the price moves throughout
    the day
    Parameters
    ----------
    df : DataFrame
        The historical stock data df

    Returns
    -------
    df : DataFrame
        The dataframe with adds columns, close_tomorrow and percentage_change
    '''
    ###Don't currently need a group by, however will be looking to explore 
    ###more tickers
    df["close_tomorrow"]=df.groupby(["ticker"])["close"].shift(-1,fill_value=np.nan)
    df["percentage_change"]=(df["close_tomorrow"]-df["close"])*100/df["close"]
    return df