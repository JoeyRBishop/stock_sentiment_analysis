'''
Functions that are required to request tweet info from twitter and save it as 
json objects
'''
import json
from datetime import datetime, timedelta
import pandas as pd
import requests
import yaml


def save_json(filename, dict_payload):
    """
    Parameters
    ----------
    filename : str
        the filename of the json file that you wish to save
    dict_payload : str
        the dict/json object to be saved

    Returns
    -------
    Saves a json file
    """
    with open(f"{filename}.json", "w+") as f:
        json.dump(dict_payload, f)


def create_query(keyword, start_date, end_date, max_results) -> dict:
    """
    Creates the params part in the GET request

    Parameters
    ----------
    keyword : str
        The key word/words that you want to be included in your search
    start_date : str
        The start of the time period that you would like twitter to search
        between.
        In the format "%Y-%m-%dT%H:%M:%S.%fZ" i.e. "2022-02-22T00:00:00.000Z"
    end_date : str
        See start date, but obviously the end of the time period
    max_results : int
        The maximum number of results that you would returned, I believe 10 is
        lowest and 100 is the highest number you cna choose

    Returns
    -------
    query : dict
        Creates the params part in the GET request
    """

    query = {
        "query": keyword,
        "start_time": start_date,
        "end_time": end_date,
        "max_results": max_results,
        "expansions": "author_id,geo.place_id,in_reply_to_user_id",
        "tweet.fields": "author_id,created_at,geo,id,in_reply_to_user_id,lang,public_metrics,referenced_tweets,reply_settings,source,text",
        "user.fields": "created_at,description,id,location,name,public_metrics,username,verified",
        "place.fields": "country,country_code,full_name,geo,id,name,place_type",
        "next_token": {},
    }
    return query


def connect_to_endpoint(url, headers, params, next_token=None) -> dict:
    """
    The GET request of the API reponse

    Parameters
    ----------
    url : str
        The URL end point that is conected too
    headers : dict
        The authorisation token {"Authorization": f"Bearer {bearer_token}"}
    params : dict
        The query payload that the API requests
    next_token : str/None, optional
        DESCRIPTION. The default is None. But can be used to scroll through
        the reponses if the API has more matches than the maximum number of
        results returned

    Returns
    -------
    response.json() : dict
        The response resposne of the API
    """
    params["next_token"] = next_token
    response = requests.request("GET", url, headers=headers, params=params)
    if response.status_code != 200:
        print("Endpoint Response Code: " + str(response.status_code))
        raise Exception(response.status_code, response.text)
    return response.json()


def end_time_calculate(start_time, days_added) -> str:
    """
    Twitter needs the date in a certain format, hence we add an int number of
    days to the start date to obtain the end date.
    In the format "%Y-%m-%dT%H:%M:%S.%fZ" i.e. "2022-02-22T00:00:00.000Z"

    Parameters
    ----------
    start_time : str
        In the format "%Y-%m-%dT%H:%M:%S.%fZ" i.e. "2022-02-22T00:00:00.000Z"
    days_added : int
        The number of days added to the start date to obtain the end date.

    Returns
    -------
    end_time : str
        The end date in correct format (see start_time)
    """
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    start_time = datetime.strptime(start_time, date_format)
    end_time = start_time + timedelta(days=days_added)
    end_time = datetime.strftime(end_time, date_format)
    return end_time


def main_api_get(start_time, bearer_token):
    """
    Parameters
    ----------
    start_time : str
        In the format "%Y-%m-%dT%H:%M:%S.%fZ" i.e. "2022-02-22T00:00:00.000Z"

    bearer_token : str
        the authorisation token that twitter required

    Returns
    -------
    json_response : TYPE
        the reponse of the API request
    """
    end_point = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    keyword = "TSLA lang:en"
    max_results = 100

    end_time = end_time_calculate(start_time, 1)

    params = create_query(keyword, start_time, end_time, max_results)
    json_response = connect_to_endpoint(end_point, headers, params)
    return json_response


def main_call_twitter_api(start_time, bearer_token):
    """
    This adds one day at the time, for 6 days, and save the returned API
    responses into a json format. Where each json file is a day

    Parameters
    ----------
    start_time : str
        In the format "%Y-%m-%dT%H:%M:%S.%fZ" i.e. "2022-02-22T00:00:00.000Z"
    bearer_token : str
        the authorisation token that twitter required

    Returns
    -------
    saves payload as json object
    """
    for i in range(6):
        try:
            payload = main_api_get(start_time, bearer_token)
            save_json(f"TSLA_{start_time[:10]}", payload)
            start_time = end_time_calculate(start_time, 1)
        except Exception as e:
            start_time = end_time_calculate(start_time, 1)
            print(e)
            

    
def main_twitter_api_call(start_time):
    ###As the twitter tokens are a secret, these are saved locally
    with open("twitter_config.yaml", "r") as ymlfile:
        config = yaml.safe_load(ymlfile)
    bearer_token = config["twitter_tokens"]["Bearer_token"]
    main_call_twitter_api(start_time, bearer_token)
