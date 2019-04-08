from . import util
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html

graph_config = {'displaylogo': False, 'modeBarButtons': [['toImage']]}


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
            html.Center(html.P(pol, style={'font-size': '75%'})),
            sentiment_graph(util.select_pol_by_name(df, pol), i)
        ]
        , className='four columns') for i, pol in enumerate(df['name'].unique())
    ])

def sentiment_graph(df, i):
    return dcc.Graph(
        config=graph_config,
        figure=update_sentiment_graph_figure(df, i)
    )

def update_slider_marks(df):
    first_date = df['date'].min()
    last_date = df['date'].max()
    return {
        util.to_timestamp(first_date): util.to_pretty_date(first_date),
        util.to_timestamp(last_date): util.to_pretty_date(last_date)
    }

def update_mention_graph_figure(df):
    data = []

    sorted_pol = df.groupby(['pol_id']).size().reset_index(name='mentions').sort_values(by='mentions', ascending=False).reset_index()
    df = df.groupby(['date', 'pol_id', 'name', 'color']).size().reset_index(name='mentions')

    first_date, last_date = df['date'].min(), df['date'].max()
    y_max = df['mentions'].max()*1.1

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
        xaxis={'range': (first_date, last_date), 'fixedrange': True},
        yaxis={'range': (0, y_max), 'fixedrange': True},
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

def update_sentiment_graph_figure(df, i):
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
