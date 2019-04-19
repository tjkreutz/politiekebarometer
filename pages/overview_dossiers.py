from src import widgets

import dash_core_components as dcc
import dash_html_components as html

from app import party_data

def get_layout():
    layout = html.Div([
        html.Div(html.H2('Dossiers'), className='title-field'),
        html.Div([
            html.P("""
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi in diam et tellus posuere fringilla ut et 
            leo. Cras porta ullamcorper nulla at tincidunt. Sed ultrices hendrerit lectus. Pellentesque egestas elit 
            lectus, vel dictum arcu ullamcorper quis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi in 
            diam et tellus posuere fringilla ut et leo. Cras porta ullamcorper nulla at tincidunt. Sed ultrices 
            hendrerit lectus. Pellentesque egestas elit lectus, vel dictum arcu ullamcorper quis.""")]
        , className='intro-text'),
        html.Hr(),
        html.Center([
            html.B("Figuur 1: "),
            html.Span("Welke dossiers werden de afgelopen 7 dagen het meest genoemd op Twitter en in het online nieuws?")
        ],className='description'),
        widgets.dossier_list(party_data),
    ])

    return layout