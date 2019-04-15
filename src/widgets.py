from . import util

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

def theme_mention_graph(id, df):
    return dcc.Graph(
        id=id,
        config=graph_config,
        figure=update_theme_mention_graph_figure(df)
    )

def pol_list(id, df, url):
    return html.Div(
        id=id,
        children=update_list_children(df, url),
    )

def theme_list(id, df):
    return html.Div(
        id=id,
        children=update_theme_list_children(df),
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
        hoverinfo='label+value',
        textinfo='percent',
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
        xaxis={'range': (0, x_max), 'fixedrange': True, 'tickformat': '%', 'hoverformat': '%', 'automargin': True, 'zeroline': False},
        yaxis={'fixedrange': True},
        autosize=True,
        margin={'l': 70, 'r': 10, 'b': 20, 't': 0},
        height=160,
    )

    return dcc.Graph(
        config=graph_config,
        figure={'data': [data], 'layout': layout})

def word_cloud(df, no=10):
    pol_id = df['pol_id'].iloc[0]

    hashtags = util.load_hashtags(pol_id).head(no)
    number = len(hashtags.index)
    if number < 5:
        return html.P('Niet genoeg data beschikbaar.', className='word-cloud-placeholder')

    hashtags['weight'] = util.min_max_normalize(hashtags['count'])
    hashtags['color'] = DEFAULT_PLOTLY_COLORS[:number]

    hashtags = hashtags.sample(frac=1).reset_index(drop=True)

    hashtags['y'] = util.sample_keyword_locations(number)

    data = go.Scatter(
        x=[i for i in range(number)],
        y=hashtags['y'],
        mode='text',
        text=hashtags['hashtag'],
        hoverinfo='text',
        marker={'opacity': 0.3},
        textfont={'size': (hashtags['weight']*6+11).astype(int), 'color': hashtags['color']},
    )

    layout = go.Layout(
        xaxis={'range': (-2, number+2), 'showgrid': False, 'showticklabels': False, 'zeroline': False, 'fixedrange': True},
        yaxis={'range': (hashtags['y'].min()-1, hashtags['y'].max()+1), 'showgrid': False, 'showticklabels': False, 'zeroline': False, 'fixedrange': True},
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
        autosize=True,
        height=100,
    )

    wc = dcc.Graph(config=graph_config, figure={'data': [data], 'layout': layout})
    return wc

def multi_party_bar_chart(df):
    df = util.select_data_sources(df, ['news'])
    df = util.select_most_mentioned_theme(df, 3)

    return html.Div([
        html.Div([
            html.Center(theme, className='description'),
            party_bar_chart(df, theme)
        ]
            , className='four columns') for i, theme in enumerate(df['theme_name'].unique())
    ])

def party_bar_chart(df, theme):
    tot_count_df = df.groupby('name').size().reset_index(name='tot_count')

    df = util.select_by_theme(df, theme)
    df = df.groupby(['name', 'color']).size().reset_index(name='count')
    df = df[df['count'] > 4]

    df = df.merge(tot_count_df, left_on='name', right_on='name')
    df['rel_count'] = df['count'] / df['tot_count']

    df = df.sort_values(by='rel_count').reset_index()

    df['party_short_name'] = df['name'].str.slice_replace(9, repl='.. ')
    df = df.iloc[-5:]

    x_max = df['rel_count'].max() + 0.01

    data = go.Bar(
        x=df['rel_count'],
        y=df['party_short_name'],
        hovertext=df['name'],
        orientation='h',
        marker={'color': df['color']},
        width=0.7,
        hoverinfo='text+x',
    )

    layout = go.Layout(
        xaxis={'range': (0, x_max), 'fixedrange': True, 'tickformat': '%', 'hoverformat': '%', 'automargin': True, 'zeroline': False},
        yaxis={'fixedrange': True},
        autosize=True,
        margin={'l': 70, 'r': 10, 'b': 20, 't': 0},
        height=160,
    )

    return dcc.Graph(
        config=graph_config,
        figure={'data': [data], 'layout': layout})

def update_breadcrumbs(pathname='/'):
    breadcrumbs = [dcc.Link('Politieke barometer', href='/')]
    if not pathname or pathname=='/':
        return breadcrumbs
    parts = ['']
    for part in pathname.split('/'):
        if part:
            parts.append(part)
            name = util.slug_to_name(part)
            breadcrumbs.append(html.Span(['  >  ', dcc.Link(name, href='/'.join(parts))]))
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

def update_theme_mention_graph_figure(df):
    data = []

    sorted_themes = df.groupby('theme_name').size().reset_index(name='mentions').sort_values(by='mentions', ascending=False).reset_index()
    df = df.groupby(['date', 'theme_name']).size().reset_index(name='mentions')

    for theme in sorted_themes['theme_name']:
        theme_df = df[df['theme_name'] == theme]
        data.append(go.Scatter(
            mode='lines',
            x=theme_df['date'],
            y=theme_df['mentions'],
            name=theme,
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
        dcc.Link([
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

def update_theme_list_children(df):
    sorted_themes = df['theme_name'].value_counts().head(5).index.tolist()
    descriptions = []

    for i, theme in enumerate(sorted_themes):
        theme_df = df[df['theme_name'] == theme]
        positive = len(theme_df.loc[theme_df['sentiment'] > 0])
        negative = len(theme_df.loc[theme_df['sentiment'] < 0])
        neutral = len(theme_df.loc[theme_df['sentiment'] == 0])
        if neutral < positive > negative:
            description = "Overwegend positieve opinies"
        elif positive < negative > neutral:
            description = "Overwegend negatieve opinies"
        else:
            description = "Overwegend neutrale opinies"
        descriptions.append(description)

    return [
        dcc.Link([
            html.Div(className='pol-picture', style={'width': '7px', 'height': '7px', 'background-color': DEFAULT_PLOTLY_COLORS[i], 'margin-top': '14px'}),
            html.P('>>', className='more-information'),
            html.Table([
                html.Tr([html.Th(str(i + 1) + '.'), html.Th(theme)]),
                html.Tr([html.Td(), html.Td(descriptions[i], style={'font-size': '60%', 'margin-bottom': '0'})]),
            ], className='pol-table'),
        ],
            href='/themas/{}'.format(util.name_to_slug(theme)),
            id='pol-item' + str(i + 1),
            className='pol-item',
        ) for i, theme in enumerate(sorted_themes)]

def update_sentiment_graph_figure(df, i=0):
    name = df['name'].iloc[0]
    color = df['color'].iloc[0]
    #todo: average sentiment in other ways?
    df.loc[df['sentiment'] > 0, 'sentiment'] = 1
    df.loc[df['sentiment'] < 0, 'sentiment'] = -1
    df = df.groupby('date')['sentiment'].mean().reset_index()

    min_sent = df['sentiment'].min()
    max_sent = df['sentiment'].max()
    if min_sent > -0.5 and max_sent < 0.5:
        min_y, max_y = -0.55, 0.55
    else:
        min_y, max_y = -1.1, 1.1

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
        yaxis={'range': (min_y, max_y), 'fixedrange': True, 'showticklabels': i==0, 'tickformat': '%', 'hoverformat': '%'},
        margin={'l': 30 if i==0 else 10, 'r': 10, 'b': 20, 't': 0},
        hovermode='closest',
        height=160,
        autosize=True,
    )}

def update_double_mention_graph_figure(news_df, tweet_df):
    news_df = news_df.groupby('date').size().reset_index(name='mentions')
    news_df = util.fill_missing_days(news_df)
    tweet_df = tweet_df.groupby('date').size().reset_index(name='mentions')
    tweet_df = util.fill_missing_days(tweet_df)

    news_trace = go.Scatter(
        mode='lines',
        x=news_df['date'],
        y=news_df['mentions'],
        name='Nieuws',
        showlegend=False,
        line={'color': '#ff7e7e'}
    )

    tweet_trace = go.Scatter(
        mode='lines',
        x=tweet_df['date'],
        y=tweet_df['mentions'],
        name='Twitter',
        showlegend=False,
        yaxis='y2',
        line={'color': '#abe2fb'},
    )

    return {
    'data': [news_trace, tweet_trace],
    'layout': go.Layout(
        xaxis={'fixedrange': True, 'automargin': True, 'showgrid': False},
        yaxis={'title': 'Aantal nieuwsartikelen', 'titlefont': {'color': '#ff7e7e'}, 'fixedrange': True, 'showgrid': False, 'automargin': True, 'rangemode': 'tozero'},
        yaxis2={'title': 'Aantal tweets', 'titlefont': {'color': '#abe2fb'}, 'side': 'right', 'fixedrange': True, 'showgrid': False, 'automargin': True, 'overlaying':'y', 'rangemode': 'tozero'},
        margin={'l': 20, 'r': 20, 'b': 20, 't': 10},
        hovermode='closest',
        autosize=True,
        height=320
    )}

