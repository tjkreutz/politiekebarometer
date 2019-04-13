import dash

from src import util
from src import widgets

import dash_html_components as html
from app import app, party_data

def get_layout():
    df = util.select_most_mentioned(party_data, n=5)

    layout = html.Div([
        html.Div([
            html.Div([
                html.Div(html.H2('Partijen'), className='title-field'),
                html.Center([html.B("Figuur 1: "), html.Span("Hoe vaak worden partijen en hun politici online genoemd?")], className='description'),
                widgets.mention_graph('party-mention-graph', df),
            ], className='eight columns'),
            html.Div([
                html.Div(html.H2('Data'), className='title-field'),
                widgets.data_checkbox('data-selector'),
                html.Div(html.H2('Periode'), className='title-field2'),
                widgets.date_slider('date-slider', df),
                html.Div(html.H2('Meest genoemd'), className='title-field2'),
                widgets.pol_list('party-list', df, 'partijen')
            ], className='four columns'),
        ], className='row'),
        html.Div([
            html.Div(html.H2([html.Span("Opinie op Twitter "), html.Span("(laatste 14 dagen)", style={'font-size': '0.9em'})]), className='title-field'),
            html.Center([html.B("Figuur 2: "), html.Span("Hoe evolueert de opinie over partijen op Twitter?")], className='description'),
            widgets.multi_sentiment_graph(df),
        ], className='row')
    ])

    return layout

@app.callback(
    dash.dependencies.Output('party-mention-graph', 'figure'),
    [dash.dependencies.Input('date-slider', 'value'),
     dash.dependencies.Input('data-selector', 'values')])
def update_party_graph(timestamp_range, data_sources):
    first_date = util.to_datetime(timestamp_range[0])
    last_date = util.to_datetime(timestamp_range[1])
    df = util.select_date_range(party_data, (first_date, last_date))
    df = util.select_data_sources(df, data_sources)
    df = util.select_most_mentioned(df, 5)
    return widgets.update_mention_graph_figure(df)

@app.callback(
    dash.dependencies.Output('party-list', 'children'),
    [dash.dependencies.Input('date-slider', 'value'),
     dash.dependencies.Input('data-selector', 'values')])
def update_party_list(timestamp_range, data_sources):
    first_date = util.to_datetime(timestamp_range[0])
    last_date = util.to_datetime(timestamp_range[1])
    df = util.select_date_range(party_data, (first_date, last_date))
    df = util.select_data_sources(df, data_sources)
    df = util.select_most_mentioned(df, 5)
    return widgets.update_list_children(df, 'partijen')
