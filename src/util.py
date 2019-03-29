import os
import time
import MySQLdb
import datetime
import pandas as pd
import random
import colorsys
from . import sql
from dotenv import load_dotenv
from urllib.parse import urlparse
from sshtunnel import SSHTunnelForwarder

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
    predefined = {'CD&V': 'cdenv', 'Ecolo-Groen': 'ecolo-groen', 'N-VA': 'n-va', 'PTB-GO!': 'ptb-go', 'PTB-PVDA-go!': 'ptb-pvda-go', 'sp.a': 'sp-a', 'Vuye&Wouters': 'vuyeenwouters'}
    if name in predefined:
        return predefined[name]
    name = name.lower()
    name = name.replace('-', '_')
    name = name.replace(' ', '-')
    return name

def slug_to_name(slug):
    predefined = {'cdenv': 'CD&V', 'ecolo-groen': 'Ecolo-Groen', 'n-va': 'N-VA', 'ptb-go': 'PTB-GO!', 'ptb-pvda-go': 'PTB-PVDA-go!', 'sp-a': 'sp.a', 'vuyeenwouters': 'Vuye&Wouters'}
    if slug in predefined:
        return predefined[slug]
    slug = slug.replace('-', ' ')
    slug = slug.replace('_', '-')
    return slug

def hex_color_to_rgb(hex_color):
    return tuple(int(hex_color[1:][i:i + 2], 16) for i in (0, 2, 4))

def rgb_to_hex_color(r, g ,b):
    return '#%02x%02x%02x' % (r, g, b)

def randomize_colors(values):
    colors = {}
    for value in values:
        h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
        r, g, b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
        hex_color = rgb_to_hex_color(r, g, b)
        colors[value] = hex_color
    return colors

def load_party(slug):
    db = get_db()
    query = sql.PROFILE_PARTY
    df = pd.read_sql(query, db, params=[slug_to_name(slug)])
    return df

def load_politician(slug):
    db = get_db()
    query = sql.PROFILE_POLITICIAN
    df = pd.read_sql(query, db, params=[slug_to_name(slug)])
    return df

def load_overview_politicians():
    db = get_db()
    query = sql.OVERVIEW_POLITICIANS
    df = pd.read_sql(query, db)
    color_dict = randomize_colors(df['pol_id'].unique())

    df['date'] = df['ts'].dt.date
    df.picture.replace([None], 'assets/blank.png', inplace=True)
    df['color'] = df.apply(lambda row: row['color'] if not pd.isnull(row['color']) else color_dict[row['pol_id']], axis=1)
    return df

def load_overview_parties():
    db = get_db()
    query = sql.OVERVIEW_PARTIES
    df = pd.read_sql(query, db)
    color_dict = randomize_colors(df['pol_id'].unique())

    df['date'] = df['ts'].dt.date
    df.picture.replace([None], 'assets/blank.png', inplace=True)
    df['color'] = df.apply(lambda row: row['color'] if not pd.isnull(row['color']) else color_dict[row['pol_id']], axis=1)
    return df

def load_most_mentioned(df, n):
    most_mentioned = df.pol_id.value_counts().head(n).index.values
    return df.loc[df['pol_id'].isin(most_mentioned)]

def load_data_sources(df, data_sources):
    if 'news' in data_sources and 'twitter' in data_sources:
        return df
    if 'news' in data_sources:
        return df.loc[df['news_id'].notnull()]
    if 'twitter' in data_sources:
        return df.loc[df['tweet_id'].notnull()]
    return df.iloc[0:0]

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
