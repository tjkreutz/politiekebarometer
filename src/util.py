import os
import time
import json
import random
import MySQLdb
import datetime
from . import sql
import pandas as pd
from dotenv import load_dotenv
from urllib.parse import urlparse

#todo: catch politician exceptions
name_exceptions = {'Marrakesh-pact': 'marrakesh_pact', 'CD&V': 'cdv', 'cdH': 'cdh', 'CSP': 'csp', 'DéFI': 'defi', 'FDF': 'fdf', 'MR': 'mr', 'N-VA': 'n_va', 'Open VLD': 'open-vld', 'PP': 'pp', 'PS': 'ps', 'PTB': 'ptb', 'PTB-GO!': 'ptb_go', 'PTB-PVDA-go!': 'ptb_pvda_go', 'PVDA': 'pvda', 'sp.a': 'spa', 'UF': 'uf', 'Vuye&Wouters': 'vuyewouters'}
slug_exceptions = {y:x for x,y in name_exceptions.items()}

def get_db():
    load_dotenv()

    database_url = os.getenv('DATABASE_URL')
    database_parse = urlparse(database_url)

    db = MySQLdb.connect(
        host=database_parse.hostname,
        user=database_parse.username,
        password=database_parse.password,
        db=database_parse.path[1:],
    )
    return db

def name_to_slug(name):
    if name in name_exceptions:
        return name_exceptions[name]
    name = name.lower()
    name = name.replace('-', '_')
    name = name.replace(' ', '-')
    return name

def slug_to_name(slug):
    if slug in slug_exceptions:
        return slug_exceptions[slug]
    slug = slug.replace('-', ' ')
    slug = slug.replace('_', '-')
    slug = slug.title()
    return slug

def fill_missing_days(df, no_of_days=30):
    start = (pd.to_datetime('today') - pd.Timedelta(days=no_of_days)).date()
    for date in pd.date_range(start, periods=no_of_days):
        if (df['date'] == date).any():
            continue
        df = df.append({'date': date, 'mentions': 0}, ignore_index=True)
    df = df.sort_values(by='date').reset_index()
    return df

def load_party_data():
    db = get_db()
    party_query = sql.PARTY_DATA
    party_df = pd.read_sql(party_query, db)
    party_pol_query = sql.PARTY_POLITICIAN_DATA
    party_pol_df = pd.read_sql(party_pol_query, db)

    df = pd.concat([party_df, party_pol_df])
    df['date'] = pd.to_datetime(df['date'].dt.date)
    df['theme_name'] = df['theme_name'].astype('category')
    df['dossier_name'] = df['dossier_name'].astype('category')
    df['picture'].fillna('/assets/blank.png', inplace=True)
    df['color'].fillna('#abe2fb', inplace=True)
    return df

def load_politician_data():
    db = get_db()
    query = sql.POLITICIAN_DATA
    df = pd.read_sql(query, db)
    df['date'] = pd.to_datetime(df['date'].dt.date)
    df['theme_name'] = df['theme_name'].astype('category')
    df['dossier_name'] = df['dossier_name'].astype('category')
    df['picture'].fillna('/assets/blank.png', inplace=True)
    df['color'].fillna('#abe2fb', inplace=True)
    return df

def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())

def sample_keyword_locations(n):
    locations, added = [], []
    available_locations = list(range(n//2))
    for i in range(n):
        if not available_locations:
            available_locations = added[:-1]
            added = []
        location = available_locations.pop(random.randrange(len(available_locations)))
        locations.append(location)
        added.append(location)
    return locations

def load_hashtags(pol_id):
    db = get_db()
    query = sql.HASHTAGS
    df = pd.read_sql(query, db, params=[pol_id])
    return df

def load_theme_profile(name):
    db = get_db()
    query = sql.THEME_PROFILE
    df = pd.read_sql(query, db, params=[name])
    return df

def select_pol_by_name(df, name):
    return df.loc[df['name']==name]

def select_by_theme(df, theme):
    return df.loc[df['theme_name']==theme]

def select_most_mentioned(df, n):
    most_mentioned = df['pol_id'].value_counts().head(n).index.tolist()
    return df.loc[df['pol_id'].isin(most_mentioned)]

def select_most_mentioned_theme(df, n):
    most_mentioned = df['theme_name'].value_counts().head(n).index.tolist()
    return df.loc[df['theme_name'].isin(most_mentioned)]

def select_data_sources(df, data_sources):
    if 'news' in data_sources and 'twitter' in data_sources:
        return df
    if 'news' in data_sources:
        return df.loc[df['news_id'].notnull()]
    if 'twitter' in data_sources:
        return df.loc[df['tweet_id'].notnull()]
    return df.iloc[0:0]

def select_last_n_days(df, no_of_days=7):
    end = pd.to_datetime('today')
    start = (end - pd.Timedelta(days=no_of_days)).date()
    return select_date_range(df, (start, end))

def select_date_range(df, date_range):
    return df.loc[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]

def to_timestamp(date):
    timestamp = int(time.mktime(date.timetuple()))
    return timestamp

def to_datetime(timestamp):
    return datetime.date.fromtimestamp(timestamp)

def to_pretty_date(date):
    return date.strftime("%d-%m")

def load_json(path):
    return json.load(open(path))
