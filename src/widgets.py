import datetime
import dash_table
from . import util
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html

graph_config = {'displaylogo': False, 'modeBarButtons': [['toImage']]}

#define custom widgets
def event_line(title, datetime):
    y = [-20+i for i in range(1000)]
    line = go.Scatter(x0=datetime, dx=0, y=y, line={'dash': 'dash', 'width': 0.5, 'color': 'black'}, showlegend=False, text='{}\n{}'.format(datetime, title), hoverinfo='text')
    return line

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

def politician_list(id, df):
    return html.Div(
        id=id,
        children=update_politician_list_children(df),
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

def politician_mention_graph(id, df):
    return dcc.Graph(
        id=id,
        config=graph_config,
        figure=update_politician_mention_graph_figure(df)
    )

#define custom interactivity
def update_politician_list_children(df):
    sorted_politicians = df.groupby(['pol_id', 'color', 'full_name']).size().reset_index(name='mentions').sort_values(by='mentions', ascending=False).reset_index()
    return [
        html.A([
            html.Img(src='assets/politician.png', className='politician-picture', style={'border': f'3px solid {politician["color"]}'}),
            html.P('>>', className='more-information'),
            html.Table([
                html.Tr([html.Th(str(index+1) + '.'), html.Th(politician['full_name'])]),
                html.Tr([html.Td(), html.Td(str(politician['mentions']) + ' keer genoemd.', style={'font-size': '60%', 'margin-bottom': '0'})]),
            ], className='politician-table'),
        ],
            href='#',
            id='politician-item' + str(index+1),
            className='politician-item',
        ) for index, politician in sorted_politicians.iterrows()]

def update_slider_marks(df):
    first_date = df['date'].min()
    last_date = df['date'].max()
    return {
        util.to_timestamp(first_date): util.to_pretty_date(first_date),
        util.to_timestamp(last_date): util.to_pretty_date(last_date)
    }

def update_politician_mention_graph_figure(df):
    data = []

    first_date, last_date = df['date'].min(), df['date'].max()

    # group by date and politician, count the rows
    sorted_politicians = df.groupby(['pol_id']).size().reset_index(name='mentions').sort_values(by='mentions', ascending=False).reset_index()
    df = df.groupby(['date', 'pol_id', 'color', 'full_name']).size().reset_index(name='mentions')


    y_max = df['mentions'].max() + 20

    for politician in sorted_politicians['pol_id']:
        politician_df = df[df['pol_id'] == politician]
        data.append(go.Scatter(
            mode='lines',
            x=politician_df['date'],
            y=politician_df['mentions'],
            name=politician_df['full_name'].iloc[0],
            #todo: Save color in relational db
            line={'color': politician_df['color'].iloc[0]},
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
