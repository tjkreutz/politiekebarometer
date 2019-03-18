import datetime
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
        values=['news', 'twitter']
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
        html.Div([
            html.Img(src='assets/politician.png', className='politician-picture', style={'border': f'solid {politician["color"]}'}),
            html.Span(str(index+1) + '. ' + politician['full_name'], className='politician-name'),
            html.P(str(politician['mentions']) + ' keer genoemd.', style={'font-size': '60%'}),
            html.A('Uitgebreide informatie >>', href='#', style={'font-size': '60%'}),
        ],
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
    df = df.groupby(['date', 'pol_id', 'color', 'full_name']).size().reset_index(name='mentions')

    y_max = df['mentions'].max() + 20

    for politician in df['pol_id'].unique():
        politician_df = df[df['pol_id'] == politician]
        data.append(go.Scatter(
            x=politician_df['date'],
            y=politician_df['mentions'],
            name=politician_df['full_name'].iloc[0],
            #todo: Save color in relational db
            line={'color': politician_df['color'].iloc[0]},
            showlegend=False,
        ))

    # custom annotated lines to demonstrate events
    schauvliege_datetime = datetime.datetime(year=2019, month=2, day=5, hour=18, minute=26)
    schauvliege_line = event_line('Joke Schauvliege neemt ontslag', schauvliege_datetime)

    francken_datetime = datetime.datetime(year=2019, month=2, day=13, hour=11)
    francken_line = event_line('Theo Francken getuigt over humanitaire visa', francken_datetime)

    data.extend([schauvliege_line, francken_line])

    return {
    'data': data,
    'layout': go.Layout(
        xaxis={'range': (first_date, last_date), 'fixedrange': True},
        yaxis={'range': (0, y_max), 'title': 'Aantal keer genoemd', 'fixedrange': True},
        margin={'l':50,'r':50,'b':20,'t':20,'pad':4},
        hovermode='closest',
    )}
