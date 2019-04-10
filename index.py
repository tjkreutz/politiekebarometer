import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from pages import home, overview_parties, overview_politicians, hoe_werkt_het, profile_party, profile_politician
from src import widgets

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Center([
            html.A([
                html.Div(html.Img(src='/assets/barometer.png'), className='barometer'),
                html.H1('De Politieke Barometer'),
            ], href='/'),
            html.Div(html.A('Partijen', href='/partijen'), className='menu-item'),
            html.Div(html.A('Politici', href='/politici'), className='menu-item'),
            html.Div(html.A("Thema's", href='#'), className='menu-item'),
            html.Div(html.A("Dossiers", href='#'), className='menu-item'),
            html.Div(html.A("Hoe werkt het?", href='/hoe-werkt-het'), className='menu-item'),
        ]),
    ], className='header'),
    html.Div([
        html.Div(widgets.breadcrumbs('breadcrumbs'), className='six columns'),
        html.Div(className='two columns'),
        html.Div(className='four columns')
    ], className='row'),
    html.Div(id='page-content'),
    html.Div([
        html.Center([
            html.P([
            """De politieke barometer is onderdeel van het """,
            html.A('NWS data', href='https://www.uantwerpen.be/nl/projecten/nws-data/'),
            """ project van de Universiteit Antwerpen en werd ontwikkeld door onderzoeksgroep """,
            html.A('CLiPS', href='https://www.uantwerpen.be/en/research-groups/clips/'),
            """."""], style={'margin-bottom': '20px'}),
        ], className='research-list')
    ], className='footer'),
], className='container')

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if not pathname or pathname=='/':
        return home.get_layout()
    elif '/partijen' in pathname:
        parts = pathname.split('/')
        if len(parts) > 2:
            return profile_party.get_layout(parts[-1])
        return overview_parties.get_layout()
    elif '/politici' in pathname:
        parts = pathname.split('/')
        if len(parts) > 2:
            return profile_politician.get_layout(parts[-1])
        return overview_politicians.get_layout()
    elif pathname == '/hoe-werkt-het':
         return hoe_werkt_het.get_layout()
    else:
        return '404. Deze pagina bestaat niet.'

@app.callback(Output('breadcrumbs', 'children'),
              [Input('url', 'pathname')])
def update_breadcrumb(pathname):
    return widgets.update_breadcrumbs(pathname)

if __name__ == '__main__':
    app.run_server()