'''
functions required to gather the stock data from yahoo finance
'''
import pandas as pd
import yfinance as yf
import numpy as np

def main_stock_data(tick="TSLA",start_date="2022-01-01",price="close"):
    '''
    Get historical stock data from yahoo finance and save it as a csv
    Parameters
    ----------
    tick : str, optional
        The ticker, The default is "TSLA".
    start_date : str, optional
        The initial start data of the histroy. The default is "2022-01-01".
    price : str, optional
         The "price" of the stock this is "subjective" as the price fluxuates
         over the day, so there is no "price for that day".
    

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
        
    df=interpolate_missing_stock_data(df,price)
    
    df=percentage_growth(df,price)
    
    df["date"]=df["date"].dt.date
    final_date=str(df["date"].max())[:10]
    df.to_csv(f"stock_data_{tick}_{final_date}.csv",index=False)
    return df



def percentage_growth(df,price):
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
    df[f"{price}_tomorrow"]=df[price].shift(-1,fill_value=np.nan)
    df["percentage_change"]=(df[f"{price}_tomorrow"]-df[price])*100/df[price]
    return df


def interpolate_missing_stock_data(df,price):
    '''
    As the stock market is closed on weekends and bank holidays, the assumption
    is made that the stock linearly increases(decreases) over the days that the
    stock market is closed.

    Parameters
    ----------
    df : DataFrame
        The dataframe that contains the stock data.
    price : str
        The column that contains the "price"

    Returns
    -------
    df_interpolate : DataFrame
        The df that contains the interpolated stock data (over the "closed"
                                                          days)

    '''
    df['date'] = pd.to_datetime(df['date']) 
    df=df.set_index("date")
    df_interpolate = df[[price]].resample('D').max()
    df_interpolate[price] = df_interpolate[price]\
    .interpolate(method='linear',limit_direction="both")
    df_interpolate=df_interpolate.reset_index()
    
    return df_interpolate
    
    
    