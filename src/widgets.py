from . import util
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html

graph_config = {'displaylogo': False, 'modeBarButtons': [['toImage']]}

#define custom widgets
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
    df = df.groupby(['date', 'politician_id']).size().reset_index(name='mentions')

    for politician in df['politician_id'].unique():
        politician_df = df[df['politician_id'] == politician]
        data.append(go.Scatter(
            x=politician_df['date'],
            y=politician_df['mentions'],
            name=politician,
        ))

    return {
    'data': data,
    'layout': go.Layout(
        xaxis={'range': (first_date, last_date), 'fixedrange': True},
        yaxis={'title': 'Aantal keer genoemd', 'fixedrange': True},
        legend={'x': 0, 'y': 1},
        margin={'l':50,'r':50,'b':20,'t':20,'pad':4},
        showlegend=True,
    )}
