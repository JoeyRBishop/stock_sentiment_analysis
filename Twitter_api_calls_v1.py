import requests
import json
import yaml
from datetime import datetime, timedelta



with open("twitter_config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile)
    
bearer_token=config["twitter_tokens"]["Bearer_token"]


def create_headers(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    return headers

def create_url(keyword, start_date, end_date, max_results = 10):
    
    search_url = "https://api.twitter.com/2/tweets/search/recent"#Change to the endpoint you want to collect data from

    #change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def end_time_calculate(start_time,days_added):
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    start_time = datetime.strptime(start_time, date_format)
    end_time=start_time+timedelta(days=days_added)
    end_time = datetime.strftime(end_time, date_format)
    return end_time



def main_api_get(start_time):
    headers = create_headers(bearer_token)
    keyword = "TSLA lang:en"
    max_results = 10
    
    end_time=end_time_calculate(start_time,1)
    
    url = create_url(keyword, start_time,end_time, max_results)
    json_response = connect_to_endpoint(url[0], headers, url[1])
    return json_response


def save_json(filename,dict_payload):
    with open(f'{filename}.json', 'w+') as f:
        json.dump(dict_payload, f)
# with open('output.json', 'r') as f:
#     data=json.load(f)    

start_time = "2022-02-22T00:00:00.000Z"
for i in range(5):
    payload=main_api_get(start_time)
    save_json(f"TSLA_{start_time[:10]}",payload)
    start_time=end_time_calculate(start_time, 1)
    

