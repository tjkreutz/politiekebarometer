from . import util

import random
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html

from plotly.colors import DEFAULT_PLOTLY_COLORS

graph_config = {'displaylogo': False, 'modeBarButtons': [['toImage']], 'locale': 'nl'}


def breadcrumbs(id):
    return html.Div(id=id, children=update_breadcrumbs(), className='breadcrumbs')

def search_bar(df, domain):
    queries = {'partijen': 'name', 'politici': 'name', 'themas': 'theme_name', 'dossiers': 'dossier_name'}
    options = df.groupby(queries[domain]).size().reset_index(name='counts').sort_values(by='counts', ascending=False).reset_index()
    options = [{'label': opt, 'value': opt} for opt in options[queries[domain]]]
    return dcc.Dropdown(
        id='search-bar',
        options=options,
        placeholder="Zoek op {}".format(domain),
        className='search-bar',
    )

def data_checkbox(id):
    return dcc.Checklist(
        id=id,
        options=[
            {'label': 'Nieuws', 'value': 'news'},
            {'label': 'Twitter', 'value': 'twitter'},
        ],
        values=['news', 'twitter'],
        className='data-checkbox',
    )

def date_slider(id, df):
    min_date = df['date'].min()
    max_date = df['date'].max()
    return dcc.RangeSlider(
        id=id,
        min=util.to_timestamp(min_date), max=util.to_timestamp(max_date),
        value=[util.to_timestamp(min_date), util.to_timestamp(max_date)],
        className='range-slider',
        allowCross=False,
        step=86400,
        marks=update_slider_marks(df)
    )

def mention_graph(id, df):
    return dcc.Graph(
        id=id,
        config=graph_config,
        figure=update_mention_graph_figure(df)
    )

def pol_list(id, df, url):
    return html.Div(
        id=id,
        children=update_list_children(df, url),
    )

def multi_sentiment_graph(df):
    df = util.select_data_sources(df, ['twitter'])
    df = util.select_most_mentioned(df, 3)
    return html.Div([
        html.Div([
            html.Center(pol, className='description'),
            sentiment_graph(util.select_pol_by_name(df, pol), i)
        ]
        , className='four columns') for i, pol in enumerate(df['name'].unique())
    ])

def sentiment_graph(df, i=0):
    return dcc.Graph(
        config=graph_config,
        figure=update_sentiment_graph_figure(df, i)
    )

def double_mention_graph(news_df, tweet_df):
    return dcc.Graph(
        config=graph_config,
        figure=update_double_mention_graph_figure(news_df, tweet_df)
    )

def sentiment_donut(df):
    colors = ['#7eff7e', '#ff7e7e', '#fff3c8']

    positive = len(df.loc[df['sentiment'] > 0])
    negative = len(df.loc[df['sentiment'] < 0])
    neutral = len(df) - positive - negative

    data = go.Pie(
        labels=['Positief', 'Negatief', 'Neutraal'],
        values=[positive, negative, neutral],
        hoverinfo='label+percent',
        textinfo='value',
        marker={'colors': colors},
        hole=0.6,
    )

    layout = go.Layout(
        autosize=True,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
        height=160,
        legend={'orientation': 'h'},
    )

    return dcc.Graph(
        config=graph_config,
        figure={'data': [data], 'layout': layout})

def theme_bar_chart(df):
    df = df.groupby('theme_name').size().reset_index(name='counts').sort_values(by='counts').reset_index()

    total_counts = df['counts'].sum()

    df['counts'] = df['counts']/total_counts
    df['theme_short_name'] = df['theme_name'].str.slice_replace(6, repl='.. ')
    df = df.iloc[-5:]

    x_max = df['counts'].max() + 0.01

    data = go.Bar(
        x=df['counts'],
        y=df['theme_short_name'],
        hovertext=df['theme_name'],
        orientation='h',
        marker={'color': '#abe2fb'},
        width=0.7,
        hoverinfo='text+x',
    )

    layout = go.Layout(
        xaxis={'range': (0, x_max), 'fixedrange': True, 'tickformat': '%', 'hoverformat': '%', 'automargin': True},
        yaxis={'fixedrange': True},
        autosize=True,
        margin={'l': 70, 'r': 10, 'b': 20, 't': 0},
        height=160,
    )

    return dcc.Graph(
        config=graph_config,
        figure={'data': [data], 'layout': layout})

def word_cloud(df, no=10):
    #todo generate words and weights from fragments
    words = ['woord']*no
    weights = [random.randint(15, 20) for i in range(no)]

    colors = [DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(no)]

    data = go.Scatter(
        x=[i for i in range(no)],
        y=random.sample([i for i in range(no)], k=no),
        mode='text',
        text=words,
        hoverinfo='text',
        marker={'opacity': 0.3},
        textfont={'size': weights, 'color': colors},
    )

    layout = go.Layout(
        xaxis={'range': (-1, no+1), 'showgrid': False, 'showticklabels': False, 'zeroline': False, 'fixedrange': True},
        yaxis={'range': (-1, no+1), 'showgrid': False, 'showticklabels': False, 'zeroline': False, 'fixedrange': True},
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
        autosize=True,
        height=100,
    )

    wc = dcc.Graph(config=graph_config, figure={'data': [data], 'layout': layout})
    return wc

def update_breadcrumbs(pathname='/'):
    breadcrumbs = [html.A('Politieke barometer', href='/')]
    if not pathname or pathname=='/':
        return breadcrumbs
    parts = ['']
    for part in pathname.split('/'):
        if part:
            parts.append(part)
            name = util.slug_to_name(part)
            breadcrumbs.append(html.Span([' ⯈ ', html.A(name, href='/'.join(parts))]))
    return breadcrumbs

def update_slider_marks(df):
    first_date = df['date'].min()
    last_date = df['date'].max()
    return {
        util.to_timestamp(first_date): util.to_pretty_date(first_date),
        util.to_timestamp(last_date): util.to_pretty_date(last_date)
    }

def update_mention_graph_figure(df):
    data = []

    sorted_pol = df.groupby('pol_id').size().reset_index(name='mentions').sort_values(by='mentions', ascending=False).reset_index()
    df = df.groupby(['date', 'pol_id', 'name', 'color']).size().reset_index(name='mentions')

    for pol in sorted_pol['pol_id']:
        pol_df = df[df['pol_id'] == pol]
        data.append(go.Scatter(
            mode='lines',
            x=pol_df['date'],
            y=pol_df['mentions'],
            name=pol_df['name'].iloc[0],
            line={'color': pol_df['color'].iloc[0]},
            showlegend=False,
        ))

    return {
    'data': data,
    'layout': go.Layout(
        xaxis={'fixedrange': True},
        yaxis={'range': (0, df['mentions'].max()*1.1), 'fixedrange': True},
        margin={'l': 30, 'r': 30, 'b': 40, 't': 30},
        hovermode='closest',
        autosize=True,
    )}

def update_list_children(df, url):
    sorted_pol = df.groupby(['pol_id', 'name', 'color', 'picture']).size().reset_index(name='mentions').sort_values(by='mentions', ascending=False).reset_index()
    return [
        html.A([
            html.Img(src=pol['picture'], className='pol-picture', style={'border': f'3px solid {pol["color"]}'}),
            html.P('>>', className='more-information'),
            html.Table([
                html.Tr([html.Th(str(index+1) + '.'), html.Th(pol['name'])]),
                html.Tr([html.Td(), html.Td(str(pol['mentions']) + ' keer genoemd.', style={'font-size': '60%', 'margin-bottom': '0'})]),
            ], className='pol-table'),
        ],
            href='/{}/{}'.format(url, util.name_to_slug(pol['name'])),
            id='pol-item' + str(index+1),
            className='pol-item',
        ) for index, pol in sorted_pol.iterrows()]

def update_sentiment_graph_figure(df, i=0):
    name = df['name'].iloc[0]
    color = df['color'].iloc[0]
    #todo: average sentiment in other ways?
    df.loc[df['sentiment'] > 0, 'sentiment'] = 1
    df.loc[df['sentiment'] < 0, 'sentiment'] = -1
    df = df.groupby('date')['sentiment'].mean().reset_index()

    trace = go.Scatter(
        mode='lines',
        x=df['date'],
        y=df['sentiment'],
        name=name,
        line={'color': color},
        showlegend=False,
    )

    return {
    'data': [trace],
    'layout': go.Layout(
        xaxis={'fixedrange': True, 'showgrid': False, 'showticklabels': False},
        yaxis={'range': (-1.1, 1.1), 'fixedrange': True, 'showticklabels': i==0, 'tickformat': '%', 'hoverformat': '%'},
        margin={'l': 30 if i==0 else 10, 'r': 10, 'b': 20, 't': 0},
        hovermode='closest',
        height=160,
        autosize=True,
    )}

def update_double_mention_graph_figure(news_df, tweet_df):
    news_df = news_df.groupby('date').size().reset_index(name='mentions')
    tweet_df = tweet_df.groupby('date').size().reset_index(name='mentions')

    news_trace = go.Scatter(
        mode='lines',
        x=news_df['date'],
        y=news_df['mentions'],
        name='Nieuws',
        showlegend=False,
        line={'color': '#b41f1f'}
    )

    tweet_trace = go.Scatter(
        mode='lines',
        x=tweet_df['date'],
        y=tweet_df['mentions'],
        name='Twitter',
        showlegend=False,
        yaxis='y2',
        line={'color': '#1f77b4'},
    )

    return {
    'data': [news_trace, tweet_trace],
    'layout': go.Layout(
        xaxis={'fixedrange': True, 'automargin': True, 'showgrid': False},
        yaxis={'title': 'Aantal nieuwsartikelen', 'titlefont': {'color': '#b41f1f'}, 'fixedrange': True, 'showgrid': False, 'automargin': True, 'rangemode': 'tozero'},
        yaxis2={'title': 'Aantal tweets', 'titlefont': {'color': '#1f77b4'}, 'side': 'right', 'fixedrange': True, 'showgrid': False, 'automargin': True, 'overlaying':'y', 'rangemode': 'tozero'},
        margin={'l': 20, 'r': 20, 'b': 20, 't': 10},
        hovermode='closest',
        autosize=True,
        height=320
    )}

