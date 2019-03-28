import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from pages import overview_parties, overview_politicians, hoe_werkt_het, profile_party, profile_politician

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Center([
            html.Div(html.Img(src='/assets/barometer.png'), className='barometer'),
            html.H1('De Politieke Barometer'),
            html.Div(html.A('Partijen', href='/partijen'), className='menu-item'),
            html.Div(html.A('Politici', href='/politici'), className='menu-item'),
            html.Div(html.A("Thema's", href='#'), className='menu-item'),
            html.Div(html.A("Dossiers", href='#'), className='menu-item'),
            html.Div(html.A("Hoe werkt het?", href='/hoe-werkt-het'), className='menu-item'),
        ]),
    ], className='header'),
    html.Div(id='page-content'),
    html.Div([
        html.Center([
            html.P("""De politieke barometer is ontwikkeld in partnerschap met verschillende onderzoeksgroepen aan de Universiteit Antwerpen.""", style={'margin-bottom': '20px'}),
            html.Span(html.A(html.Img(src='https://www.uantwerpen.be/images/uantwerpen/container1186/images/UA_HOR_NED_RGB.png', style={'height': '32px'}), href='https://www.uantwerpen.be/')),
            html.Span(html.A(html.Img(src='/assets/m2p.png', style={'height': '32px'}), href="https://www.uantwerpen.be/nl/onderzoeksgroep/m2p/")),
            html.Span(html.A(html.Img(src='/assets/mpc.png', style={'height': '32px'}), href="https://www.uantwerpen.be/nl/onderzoeksgroep/mpc/")),
            html.Span(html.A(html.Img(src='/assets/clips.png', style={'height': '32px'}), href="https://www.uantwerpen.be/nl/onderzoeksgroep/clips/")),
        ], className='research-list')
    ], className='footer'),
], className='container')

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if not pathname or pathname=='/':
        return overview_parties.layout
    elif '/partijen' in pathname:
        parts = pathname.split('/')
        if len(parts) > 2:
            return profile_party.get_layout(parts[-1])
        return overview_parties.layout
    elif '/politici' in pathname:
        parts = pathname.split('/')
        if len(parts) > 2:
            return profile_politician.get_layout(parts[-1])
        return overview_politicians.layout
    elif pathname == '/hoe-werkt-het':
         return hoe_werkt_het.layout
    else:
        return '404. Deze pagina bestaat niet.'

if __name__ == '__main__':
    app.run_server(debug=True)