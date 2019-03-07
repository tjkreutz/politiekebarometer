import time
import datetime
import pandas as pd

def load_data():
    #todo load using sql
    df = pd.read_csv('data/politician_mention.csv')
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    return df

def load_most_mentioned(df, n):
    most_mentioned = df.politician_id.value_counts().head(n).index.values
    return df.loc[df['politician_id'].isin(most_mentioned)]

def load_days(df, days):
    last_date = df['date'].max()
    first_date = last_date - datetime.timedelta(days=days)
    return load_date_range(df, (first_date, last_date))

def load_date_range(df, date_range):
    return df.loc[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]

def to_timestamp(date):
    timestamp = int(time.mktime(date.timetuple()))
    return timestamp

def to_datetime(timestamp):
    return datetime.date.fromtimestamp(timestamp)

def to_pretty_date(date):
    return date.strftime("%d-%m")
