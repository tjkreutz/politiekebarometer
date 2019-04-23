from src import widgets

import dash_core_components as dcc
import dash_html_components as html

from app import party_data

def get_layout():
    layout = html.Div([
        html.Div(html.H2('Dossiers'), className='title-field'),
        html.Div([
            html.P("""
            Met de nieuwsdossiers volgen we langlopende gebeurtenissen die invloed kunnen hebben op de politieke 
            agenda. We laten onder andere zien welke dossiers momenteel het vaakst genoemd worden in het nieuws en op 
            Twitter en welke partijen en politici vaak in dezelfde berichten voorkomen.""")
        ]
        , className='intro-text'),
        html.Hr(style={'margin': '10px'}),
        html.Center([
            html.B("Figuur 1: "),
            html.Span("Welke dossiers werden de laatste 30 dagen het meest genoemd op Twitter en in het online nieuws?")
        ],className='description'),
        widgets.dossier_list(party_data),
    ])

    return layout