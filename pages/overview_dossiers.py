from src import widgets

import dash_core_components as dcc
import dash_html_components as html

from app import party_data

def get_layout():
    layout = html.Div([
        html.Div(html.H2('Dossiers'), className='title-field'),
        html.Div([html.P("""Dummy intro.""")]
        , className='intro-text'),
        html.Hr(),
        html.Center([
            html.B("Figuur 1: "),
            html.Span("Welke dossiers werden de afgelopen 7 dagen het meest genoemd op Twitter en in het online nieuws?")
        ],className='description'),
        widgets.dossier_list(party_data),
    ])

    return layout