"""
converts the api payloads (json) into a dataframe
"""
import json
from datetime import datetime
from glob import glob

import pandas as pd


def twitter_date2dt(df, header):
    """
    converts "twitter time" into datetime

    Parameters
    ----------
    df : DateFrame
        The df
    header : str
        The header of the column that you wish to convert

    Returns
    -------
    column : Series
        Where the elements are datetime in the form "YYYY-mm-dd HH:MM:SS"
    """
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    column = df[header].apply(lambda x: datetime.strptime(x, date_format))
    column = column.dt.date
    return column


def main_json2pd(path_input, dates):
    """
    Reads all json file and returns a df of "useful" infomation

    Parameters
    ----------
    path_input : str
        the path to the folder of json files

    Returns
    -------
    df : DataFrame
        The master dataframe which combines all the json files into one df
    """

    all_df = dict()
    for date in dates:
        path = f"TSLA_{date[:10]}.json"
        print(path)
        ###read all json files in the path_input
        with open(path, "r") as read_file:
            json_twitter = json.load(read_file)
        ###json_twitter is a dict, where two parts need flattening
        df_data = pd.json_normalize(json_twitter["data"])
        df_person = pd.json_normalize(json_twitter["includes"]["users"])
        ###Rename columns to allow a merge
        df_person = df_person.rename(
            columns={"created_at": "account_created_at", "id": "author_id"}
        )
        df = pd.merge(df_data, df_person, on=["author_id"])
        ###Drop any blank tweets
        df = df.dropna(subset=["text"])

        all_df[path] = df
    df = pd.concat(all_df)
    ###Making columns more usable
    df["date"] = twitter_date2dt(df, "created_at")
    df = df.drop(columns=["created_at"])

    df["account_created_at"] = twitter_date2dt(df, "account_created_at")
    return df
