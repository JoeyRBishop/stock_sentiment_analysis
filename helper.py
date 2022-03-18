import os
from datetime import date, datetime, timedelta


def date_to_download():
    already_present_date = []
    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    for f in files:
        if len(f) == 20 and f[:5] == "TSLA_" and f[15:] == ".json":
            already_present_date.append(f[5:15])

    last_6_dates = []
    today = date.today()
    for i in range(6):
        past_dates = today - timedelta(i + 1)
        last_6_dates.append(past_dates.strftime("%Y-%m-%d"))

    return list(set(last_6_dates).difference(already_present_date))
