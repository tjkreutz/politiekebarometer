import dash_core_components as dcc
import dash_html_components as html

from pages import overview_parties

def get_layout():
    layout = html.Div([
        html.Div([
            html.Div(html.H2('Wat is de politieke barometer?'), className='title-field'),
            html.P("""
            De politieke barometer verwerkt ongeveer 1.000 nieuwsartikelen en meer dan 200.000 tweets over politici 
            en politieke partijen per dag. Dat gebeurt automatisch met behulp van een computerprogramma dat de tekst 
            taalkundig analyseert.
            """),
            html.P([
                html.Span("De barometer laat toe om doorheen de tijd het aantal vermeldingen te traceren van "),
                dcc.Link("partijen", href='/partijen'),
                html.Span(", "),
                dcc.Link("politici", href='/politici'),
                html.Span(" en "),
                dcc.Link("nieuwsdossiers", href='/dossiers'),
                html.Span(""" 
                en het sentiment van die vermeldingen (positief, negatief of neutraal). Op die manier kan u de politieke 
                "buzz" op twitter en online nieuws opvolgen.
                """)
            ]),
            html.P([
                """Heeft u vragen of opmerking over de Politieke Barometer? Stuur ons een email (""",
                html.A("nwsdata@uantwerpen.be", href='mailto:nwsdata@uantwerpen.be'),
                ")."
            ]),
        ], className='intro-text'),
        overview_parties.get_layout(),
    ])

    return layout
