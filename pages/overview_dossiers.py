import dash_core_components as dcc
import dash_html_components as html

def get_layout():
    layout = html.Div([
        html.Div(html.H2('Dossiers'), className='title-field'),
        html.Div([html.P("""Dummy intro.""")]
        , className='intro-text'),
        html.Hr(),
        html.Center([
            html.B("Figuur 1: "),
            html.Span("Welke dossiers werden de afgelopen 7 dagen vaakst genoemd op Twitter en in het online nieuws?")
        ],className='description'),
        dcc.Link(
            html.Div([
                html.Div([
                    html.H2('1. Brexit (700)')
                ], className='top-bar'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Img(src='/assets/brexit.jpg'),
                            html.P("""
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vel imperdiet metus, cursus 
                            condimentum orci. Mauris aliquet metus elit... 
                            """),
                        ], className='eight columns'),
                        html.P("""
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vel imperdiet metus, cursus 
                        condimentum orci.
                        """, className='four columns'),
                    ], className='row')
                ], className='bottom-content'),
            ], className='dossier')
        , href='#'),
    ])

    return layout