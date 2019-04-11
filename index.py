import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server, party_data, politician_data
from pages import home, overview_parties, overview_politicians, hoe_werkt_het, profile_party, profile_politician
from src import util, widgets

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Center([
            dcc.Link([
                html.Div(html.Img(src='/assets/barometer.png'), className='barometer'),
                html.H1('De Politieke Barometer'),
            ], href='/'),
            html.Div(dcc.Link('Partijen', href='/partijen'), className='menu-item'),
            html.Div(dcc.Link('Politici', href='/politici'), className='menu-item'),
            html.Div(dcc.Link("Thema's", href='#'), className='menu-item'),
            html.Div(dcc.Link("Dossiers", href='#'), className='menu-item'),
            html.Div(dcc.Link("Hoe werkt het?", href='/hoe-werkt-het'), className='menu-item'),
        ]),
    ], className='header'),
    html.Div(
        html.Div([
            html.Div(widgets.breadcrumbs('breadcrumbs'), className='eight columns'),
            html.Div(html.Div(dcc.Dropdown(id='search-bar', className='search-bar', placeholder='Zoek'), id='search-bar-holder'), className='four columns'),
        ], className='row'),
        className='search-container'),
    html.Div(id='page-content'),
    html.Div([
        html.Center([
            html.P([
            """De politieke barometer is onderdeel van het """,
            dcc.Link('NWS data', href='https://www.uantwerpen.be/nl/projecten/nws-data/'),
            """ project van de Universiteit Antwerpen en werd ontwikkeld door onderzoeksgroep """,
            dcc.Link('CLiPS', href='https://www.uantwerpen.be/en/research-groups/clips/'),
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

@app.callback(Output('search-bar-holder', 'children'),
              [Input('url', 'pathname')])
def update_search_bar(pathname):
    if not pathname or pathname=='/' or 'partijen' in pathname:
        return [widgets.search_bar(party_data, 'partijen')]
    if 'politici' in pathname:
        return [widgets.search_bar(politician_data, 'politici')]
    if 'themas' in pathname:
        return []
    if 'dossiers' in pathname:
        return []
    return []

@app.callback(Output('url', 'pathname'),
              [Input('search-bar', 'value')])
def search(value):
    if not value:
        return None
    if value in party_data['name'].unique():
        return '/partijen/{}'.format(util.name_to_slug(value))
    if value in politician_data['name'].unique():
        return '/politici/{}'.format(util.name_to_slug(value))
    if value in party_data['theme_name'].unique():
        return '/themas/{}'.format(util.name_to_slug(value))
    return None

if __name__ == '__main__':
    app.run_server()