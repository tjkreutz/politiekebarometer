import dash

from src import util
from src import widgets

import dash_html_components as html
from app import app, overview_politicians

def get_layout():
    df = util.select_most_mentioned(overview_politicians, n=5)

    layout = html.Div([
        html.Div([
            html.Div([
                html.Div(html.H2('Politici'), className='title-field'),
                html.Center(html.P([html.B("Figuur 2: "), html.Span("Hoe vaak worden politici online genoemd?")], style={'font-size': '75%'})),
                widgets.politician_mention_graph('politician-mention-graph', df),
            ], className='eight columns'),
            html.Div([
                html.Div(html.H2('Data'), className='title-field'),
                widgets.data_checkbox('data-selector'),
                html.Div(html.H2('Periode'), className='title-field'),
                widgets.date_slider('date-slider', df),
                html.Div(html.H2('Meest genoemd'), className='title-field'),
                widgets.politician_list('politician-list', df)
            ], className='four columns'),
        ], className='row'),
    ])

    return layout

@app.callback(
    dash.dependencies.Output('politician-mention-graph', 'figure'),
    [dash.dependencies.Input('date-slider', 'value'),
     dash.dependencies.Input('data-selector', 'values')])
def update_politician_graph(timestamp_range, data_sources):
    first_date = util.to_datetime(timestamp_range[0])
    last_date = util.to_datetime(timestamp_range[1])
    df = util.select_date_range(overview_politicians, (first_date, last_date))
    df = util.select_data_sources(df, data_sources)
    df = util.select_most_mentioned(df, 5)
    return widgets.update_mention_graph_figure(df)

@app.callback(
    dash.dependencies.Output('politician-list', 'children'),
    [dash.dependencies.Input('date-slider', 'value'),
     dash.dependencies.Input('data-selector', 'values')])
def update_politician_list(timestamp_range, data_sources):
    first_date = util.to_datetime(timestamp_range[0])
    last_date = util.to_datetime(timestamp_range[1])
    df = util.select_date_range(overview_politicians, (first_date, last_date))
    df = util.select_data_sources(df, data_sources)
    df = util.select_most_mentioned(df, 5)
    return widgets.update_list_children(df, 'politici')
