'''
The main script that runs them all
'''
from twitter_api_call import main_twitter_api_call
from json2pd import main_json2pd
from stock_data import main_stock_data


if __name__ == "__main__":
    
    main_twitter_api_call("2022-02-28T00:00:00.000Z")
    df_twitter=main_json2pd("")
    
    df_stock=main_stock_data("TSLA","2022-01-01")
