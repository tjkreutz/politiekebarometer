import time
import numpy
import datetime
import pandas as pd
import random
import colorsys

def hex_color_to_rgb(hex_color):
    return tuple(int(hex_color[1:][i:i + 2], 16) for i in (0, 2, 4))

def rgb_to_hex_color(r, g ,b):
    return '#%02x%02x%02x' % (r, g, b)

def lighten_hex_color(hex_color):
    r, g, b =hex_color_to_rgb(hex_color)
    color = numpy.array([r, g, b])
    white = numpy.array([255, 255, 255])
    r, g, b = color + (white - color) * 0.75
    return rgb_to_hex_color(int(r), int(g), int(b))

def randomize_colors(values):
    colors = {}
    for value in values:
        h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
        r, g, b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
        hex_color = rgb_to_hex_color(r, g, b)
        colors[value] = hex_color
    return colors

def load_data():
    #todo load using sql
    df = pd.read_csv('data/politician_mention.csv')
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    color_dict = randomize_colors(df['politician_id'].unique())
    df['color'] = df.apply(lambda row: color_dict[row['politician_id']], axis=1)
    return df

def load_most_mentioned(df, n):
    most_mentioned = df.politician_id.value_counts().head(n).index.values
    return df.loc[df['politician_id'].isin(most_mentioned)]

def load_data_sources(df, data_sources):
    return df.loc[df['genre'].isin(data_sources)]

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
