import dash

from src import util
from src import widgets

import dash_html_components as html
from app import app

# load data
og_df = util.load_parties()
df = util.load_most_mentioned(og_df, n=5)

# define layout
layout = html.Div([
    html.Div([
        html.P("""
        De politieke barometer verwerkt ongeveer 1.000 nieuwsartikelen en meer dan 200.000 tweets over politici 
        en politieke partijen per dag. Dat gebeurt automatisch met behulp van een computerprogramma dat de tekst 
        taalkundig analyseert."""),
    ], className='intro-text'),
    html.Div([
        html.Div([
            html.Div(html.H2('Partijen'), className='title-field'),
            widgets.party_mention_graph('party-mention-graph', df),
            html.Center(html.P([html.B("Figuur 1: "), html.Span("Hoe vaak worden partijen online genoemd?")], style={'font-size': '75%'})),
        ], className='eight columns'),
        html.Div([
            html.Div(html.H2('Data'), className='title-field'),
            widgets.data_checkbox('data-selector'),
            html.Div(html.H2('Periode'), className='title-field'),
            widgets.date_slider('date-slider', df),
            html.Div(html.H2('Meest genoemd'), className='title-field'),
            widgets.party_list('party-list', df)
        ], className='four columns'),
    ], className='row'),
])

@app.callback(
    dash.dependencies.Output('party-mention-graph', 'figure'),
    [dash.dependencies.Input('date-slider', 'value'),
     dash.dependencies.Input('data-selector', 'values')])
def update_party_graph(timestamp_range, data_sources):
    first_date = util.to_datetime(timestamp_range[0])
    last_date = util.to_datetime(timestamp_range[1])
    df = util.load_most_mentioned(og_df, 5)
    df = util.load_date_range(df, (first_date, last_date))
    df = util.load_data_sources(df, data_sources)
    return widgets.update_party_mention_graph_figure(df)

@app.callback(
    dash.dependencies.Output('party-list', 'children'),
    [dash.dependencies.Input('date-slider', 'value'),
     dash.dependencies.Input('data-selector', 'values')])
def update_party_list(timestamp_range, data_sources):
    first_date = util.to_datetime(timestamp_range[0])
    last_date = util.to_datetime(timestamp_range[1])
    df = util.load_most_mentioned(og_df, 5)
    df = util.load_date_range(df, (first_date, last_date))
    df = util.load_data_sources(df, data_sources)
    return widgets.update_party_list_children(df)
