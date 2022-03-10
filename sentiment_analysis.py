'''
Preparing the data for the model
'''
from transformers import pipeline
###initalise the sentiment model
sentiment_analiser = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english")

def main_sentiment_analysis(tweets):
    '''
    Takes a list of tweets and classifies them into 0 (negative) or 
    1 (posivite)
    Parameters
    ----------
    tweets : list
        A list of tweets (str)

    Returns
    -------
    classification : int
        Either 0 (negative) or 1 (positive)

    '''
    sentiments=sentiment_analiser(tweets)
    classification=[1 if x["label"]=="POSITIVE" else 0 for x in sentiments]
    return classification 
        
    
