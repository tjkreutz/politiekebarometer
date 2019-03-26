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
app.title = 'De Politieke Barometer'
app.layout = html.Div([
    html.Script(src='https://cdn.plot.ly/plotly-locale-nl-latest.js'),
    html.Div([
        html.Center([
            html.Div(html.Img(src='assets/barometer.png'), className='barometer'),
            html.H1('De Politieke Barometer'),
            html.Div(html.A("Hoe werkt het?", href='#'), className='menu-item'),
            html.Div(html.A('Partijen', href='#'), className='menu-item'),
            html.Div(html.A('Politici', href='#'), className='menu-item'),
            html.Div(html.A("Thema's", href='#'), className='menu-item'),
            html.Div(html.A("Dossiers", href='#'), className='menu-item'),
        ]),
        html.Div([
            html.P("""
            De politieke barometer verwerkt ongeveer 1.000 nieuwsartikelen en meer dan 200.000 tweets over politici 
            en politieke partijen per dag. Dat gebeurt automatisch met behulp van een computerprogramma dat de tekst 
            taalkundig analyseert."""),
        ], className='intro-text'),
        html.Div([
            html.Div([
                html.Div(html.H2('Politici'), className='header'),
                widgets.politician_mention_graph('politician-mention-graph', df),
                html.Center(html.P([html.B("Figuur 1: "), html.Span("Hoe vaak worden politici online genoemd?")], style={'font-size': '75%'})),
            ], className='eight columns'),
            html.Div([
                html.Div(html.H2('Data'), className='header'),
                widgets.data_checkbox('data-selector'),
                html.Div(html.H2('Periode'), className='header'),
                widgets.date_slider('date-slider', df),
                html.Div(html.H2('Meest genoemd'), className='header'),
                widgets.politician_list('politician-list', df)
            ], className='four columns'),
        ], className='row'),
        html.Div([
            html.Center([
                html.P("""De politieke barometer is ontwikkeld in partnerschap met verschillende onderzoeksgroepen aan de Universiteit Antwerpen.""", style={'margin-bottom': '20px'}),
                html.Span(html.A(html.Img(src='https://www.uantwerpen.be/images/uantwerpen/container1186/images/UA_HOR_NED_RGB.png', style={'height': '32px'}), href='https://www.uantwerpen.be/')),
                html.Span(html.A(html.Img(src='assets/m2p.png', style={'height': '32px'}), href="https://www.uantwerpen.be/nl/onderzoeksgroep/m2p/")),
                html.Span(html.A(html.Img(src='assets/mpc.png', style={'height': '32px'}), href="https://www.uantwerpen.be/nl/onderzoeksgroep/mpc/")),
                html.Span(html.A(html.Img(src='assets/clips.png', style={'height': '32px'}), href="https://www.uantwerpen.be/nl/onderzoeksgroep/clips/")),
            ], className='research-list')
        ], className='footer'),
    ], className='container')
])

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
    [dash.dependencies.Input('date-slider', 'value'),
     dash.dependencies.Input('data-selector', 'values')])
def update_graph(timestamp_range, data_sources):
    first_date = util.to_datetime(timestamp_range[0])
    last_date = util.to_datetime(timestamp_range[1])
    df = util.load_most_mentioned(og_df, 5)
    df = util.load_date_range(df, (first_date, last_date))
    df = util.load_data_sources(df, data_sources)
    return widgets.update_politician_mention_graph_figure(df)

@app.callback(
    dash.dependencies.Output('politician-list', 'children'),
    [dash.dependencies.Input('date-slider', 'value'),
     dash.dependencies.Input('data-selector', 'values')])
def update_politician_list(timestamp_range, data_sources):
    first_date = util.to_datetime(timestamp_range[0])
    last_date = util.to_datetime(timestamp_range[1])
    df = util.load_most_mentioned(og_df, 5)
    df = util.load_date_range(df, (first_date, last_date))
    df = util.load_data_sources(df, data_sources)
    return widgets.update_politician_list_children(df)

if __name__ == '__main__':
    app.run_server(debug=True)
