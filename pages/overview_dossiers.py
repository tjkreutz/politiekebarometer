import dash_html_components as html

def get_layout():
    layout = html.Div([
        html.Div([html.P("""Dummy intro.""")]
        , className='intro-text'),
        html.Hr(),
        html.Div(html.H2('Dossiers'), className='title-field'),
        html.Div([
            html.Div([
                html.Div('dossier1', className='dossier')
            ], className='six columns'),
            html.Div([
                html.Div('dossier2', className='dossier')
            ], className='six columns')
        ], className='row'),
        html.Div([
            html.Div([
                html.Div('dossier3', className='dossier')
            ], className='six columns'),
            html.Div([
                html.Div('dossier4', className='dossier')
            ], className='six columns')
        ], className='row')
    ])

    return layout