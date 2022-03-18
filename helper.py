import os
from datetime import date, datetime, timedelta


def date_to_download():
    '''
    
    Will get today's date and then generates a list of the last six days 
    and compares this to the dates already gathered and returns the dates that
    needs to be gathered.
    
    Returns
    -------
    list of str, which are dates to be gathered

    '''    
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
    
    dates2download=list(set(last_6_dates).difference(already_present_date))

    return dates2download
