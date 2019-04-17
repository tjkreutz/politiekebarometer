import dash

from src import util
from src import widgets

import dash_html_components as html
from app import app, party_data

def get_layout():
    df = util.select_most_mentioned_theme(party_data, n=5)

    layout = html.Div([
        html.Div([
            html.Div([
                html.Div(html.H2("Thema's"), className='title-field'),
                html.Center([html.B("Figuur 1: "), html.Span("Over welke politieke thema's wordt het vaakst geschreven?")], className='description'),
                widgets.theme_mention_graph('theme-mention-graph', df),
            ], className='eight columns'),
            html.Div([
                html.Div(html.H2('Data'), className='title-field'),
                widgets.data_checkbox('data-selector'),
                html.Div(html.H2('Periode'), className='title-field2'),
                widgets.date_slider('date-slider', df),
                html.Div(html.H2('Meest genoemd'), className='title-field2'),
                widgets.theme_list('theme-list', df)
            ], className='four columns'),
        ], className='row'),
        html.Div([
            html.Div(html.H2("Partijen en thema's in het nieuws"), className='title-field'),
            html.Center([html.B("Figuur 2: "), html.Span("Bij welke partijen gaat de berichtgeving in het nieuws relatief vaak over deze thema's?")], className='description'),
            widgets.multi_party_bar_chart(df),
        ], className='row')
    ])

    return layout

@app.callback(
    dash.dependencies.Output('theme-mention-graph', 'figure'),
    [dash.dependencies.Input('date-slider', 'value'),
     dash.dependencies.Input('data-selector', 'values')])
def update_theme_graph(timestamp_range, data_sources):
    first_date = util.to_datetime(timestamp_range[0])
    last_date = util.to_datetime(timestamp_range[1])
    df = util.select_date_range(party_data, (first_date, last_date))
    df = util.select_data_sources(df, data_sources)
    df = util.select_most_mentioned_theme(df, 5)
    return widgets.update_theme_mention_graph_figure(df)

@app.callback(
    dash.dependencies.Output('theme-list', 'children'),
    [dash.dependencies.Input('date-slider', 'value'),
     dash.dependencies.Input('data-selector', 'values')])
def update_theme_list(timestamp_range, data_sources):
    first_date = util.to_datetime(timestamp_range[0])
    last_date = util.to_datetime(timestamp_range[1])
    df = util.select_date_range(party_data, (first_date, last_date))
    df = util.select_data_sources(df, data_sources)
    df = util.select_most_mentioned_theme(df, 5)
    return widgets.update_theme_list_children(df)
