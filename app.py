import dash

from src import util
from src import widgets

import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# load data
og_df = util.load_data()
df = util.load_most_mentioned(og_df, n=5)

# define layout
app.layout = html.Div([
    html.Center([
        html.H1('De Politieke Barometer'),
        html.Div(html.A('Partijen', href='#'), className='menu-item'),
        html.Div(html.A('Politici', href='#'), className='menu-item'),
        html.Div(html.A("Thema's", href='#'), className='menu-item'),
        html.Div(html.A("Dossiers", href='#'), className='menu-item'),
    ]),
    html.Div([
        html.P("De politieke barometer verwerkt ongeveer 1.000 nieuwsartikelen en meer dan 200.000 tweets per dag. Met een computerprogramma analyseren we de context waarin politieke spelers voorkomen. Wordt er vooral positief of negatief over hen geschreven, en met welke politieke thema's worden zij vaak genoemd?"""),
    ], className='intro-text'),
    html.Div([
        html.Div([
            html.Div(html.H2('Politici'), className='header'),
            widgets.politician_mention_graph('politician-mention-graph', df),
        ], className='eight columns'),
        html.Div([
            html.Div(html.H2('Periode'), className='header'),
            widgets.date_slider('date-slider', df),
            html.Div(html.H2('Meest genoemd'), className='header'),
        ], className='four columns'),
    ], className='row'),
], className='container')


# define widget interactivity
@app.callback(
    dash.dependencies.Output('date-slider', 'marks'),
    [dash.dependencies.Input('date-slider', 'value')])
def update_slider(timestamp_range):
    first_date = util.to_datetime(timestamp_range[0])
    last_date = util.to_datetime(timestamp_range[1])
    df = util.load_most_mentioned(og_df, 5)
    df = util.load_date_range(df, (first_date, last_date))
    return widgets.update_slider_marks(df)

@app.callback(
    dash.dependencies.Output('politician-mention-graph', 'figure'),
    [dash.dependencies.Input('date-slider', 'value')])
def update_graph(timestamp_range):
    first_date = util.to_datetime(timestamp_range[0])
    last_date = util.to_datetime(timestamp_range[1])
    df = util.load_most_mentioned(og_df, 5)
    df = util.load_date_range(df, (first_date, last_date))
    return widgets.update_politician_mention_graph_figure(df)

if __name__ == '__main__':
    app.run_server(debug=True)
