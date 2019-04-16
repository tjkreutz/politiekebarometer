import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server, party_data, politician_data
from pages import home, overview_parties, overview_politicians, overview_themes, profile_party, profile_politician, profile_theme, hoe_werkt_het
from src import util, widgets

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div(
            dcc.Link([
                html.Div(html.Img(src='/assets/barometer.png'), className='barometer'),
                html.H1('De Politieke Barometer'),
            ], href='/')
        , className='logo'),
        html.H2('Wat wordt er in online media geschreven over de politieke partijen?'),
    ], className='header'),
    html.Div([
        html.Div([
            dcc.Link(html.Div("Partijen", className='menu-item'), href='/partijen'),
            dcc.Link(html.Div("Politici", className='menu-item'), href='/politici'),
            dcc.Link(html.Div("Thema's", className='menu-item'), href='/themas'),
            dcc.Link(html.Div("Dossiers", className='menu-item'), href='#'),
            dcc.Link(html.Div("Hoe werkt het?", className='menu-item'), href='/hoe-werkt-het'),
        ], className='menu'),
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
                html.A('NWS data', href='https://www.uantwerpen.be/nl/projecten/nws-data/', target="_blank"),
                """ project van de Universiteit Antwerpen en werd ontwikkeld door onderzoeksgroep """,
                html.A('CLiPS', href='https://www.uantwerpen.be/en/research-groups/clips/', target="_blank"),
                """."""], style={'margin-bottom': '20px'}),
            ], className='research-list')
        ], className='footer'),
    ], className='container')
])

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
    elif '/themas' in pathname:
        parts = pathname.split('/')
        if len(parts) > 2:
            return profile_theme.get_layout(parts[-1])
        return overview_themes.get_layout()
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
    if not pathname or pathname=='/' or '/partijen' in pathname:
        return [widgets.search_bar(party_data, 'partijen')]
    if '/politici' in pathname:
        return [widgets.search_bar(politician_data, 'politici')]
    if '/themas' in pathname:
        return [widgets.search_bar(party_data, "thema's")]
    if '/dossiers' in pathname:
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
    app.run_server(debug=True)