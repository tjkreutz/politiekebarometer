import os
import time
import MySQLdb
import datetime
from . import sql
import pandas as pd
from dotenv import load_dotenv
from urllib.parse import urlparse
from sshtunnel import SSHTunnelForwarder

#todo: catch politician exceptions
name_exceptions = {'CD&V': 'cdv', 'cdH': 'cdh', 'CSP': 'csp', 'DéFI': 'defi', 'FDF': 'fdf', 'MR': 'mr', 'N-VA': 'n_va', 'Open VLD': 'open-vld', 'PP': 'pp', 'PS': 'ps', 'PTB': 'ptb', 'PTB-GO!': 'ptb_go', 'PTB-PVDA-go!': 'ptb_pvda_go', 'PVDA': 'pvda', 'sp.a': 'spa', 'UF': 'uf', 'Vuye&Wouters': 'vuyewouters'}
slug_exceptions = {y:x for x,y in name_exceptions.items()}

def get_db():
    load_dotenv()

    ssh_url = os.getenv('SSH_URL')
    ssh_parse = urlparse(ssh_url)
    ssh_private_key = os.getenv('SSH_PRIVATE_KEY')
    ssh_private_key_password = os.getenv('SSH_PRIVATE_KEY_PASSWORD')

    database_url = os.getenv('DATABASE_URL')
    database_parse = urlparse(database_url)

    tunnel = SSHTunnelForwarder(
            (ssh_parse.hostname, ssh_parse.port),
            ssh_username=ssh_parse.username,
            ssh_password=ssh_parse.password,
            ssh_pkey=ssh_private_key,
            ssh_private_key_password=ssh_private_key_password,
            remote_bind_address=(database_parse.hostname, database_parse.port))
    tunnel.start()
    db = MySQLdb.connect(
        host='127.0.0.1',
        user=database_parse.username,
        password=database_parse.password,
        db=database_parse.path[1:],
        port=tunnel.local_bind_port,
        ssl={
        'ca': 'assets/ca.pem',
        'cert': 'assets/client-cert.pem',
        'key': 'assets/client-key.pem',
        }
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

def fill_missing_days(df, no_of_days=14):
    start = (pd.to_datetime('today') - pd.Timedelta(days=no_of_days)).date()
    for date in pd.date_range(start, periods=no_of_days+1):
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
    df['picture'].fillna('/assets/blank.png', inplace=True)
    df['color'].fillna('#abe2fb', inplace=True)
    return df

def load_politician_data():
    db = get_db()
    query = sql.POLITICIAN_DATA
    df = pd.read_sql(query, db)
    df['date'] = pd.to_datetime(df['date'].dt.date)
    df['theme_name'] = df['theme_name'].astype('category')
    df['picture'].fillna('/assets/blank.png', inplace=True)
    df['color'].fillna('#abe2fb', inplace=True)
    return df

def select_pol_by_name(df, name):
    return df.loc[df['name']==name]

def select_most_mentioned(df, n):
    most_mentioned = df.pol_id.value_counts().head(n).index.values
    return df.loc[df['pol_id'].isin(most_mentioned)]

def select_data_sources(df, data_sources):
    if 'news' in data_sources and 'twitter' in data_sources:
        return df
    if 'news' in data_sources:
        return df.loc[df['news_id'].notnull()]
    if 'twitter' in data_sources:
        return df.loc[df['tweet_id'].notnull()]
    return df.iloc[0:0]

def select_date_range(df, date_range):
    return df.loc[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]

def to_timestamp(date):
    timestamp = int(time.mktime(date.timetuple()))
    return timestamp

def to_datetime(timestamp):
    return datetime.date.fromtimestamp(timestamp)

def to_pretty_date(date):
    return date.strftime("%d-%m")
