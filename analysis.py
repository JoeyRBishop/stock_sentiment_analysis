import pandas as pd

def quick_pandas():
    file = pd.read_csv("labeled_classified_tweets.csv")
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

