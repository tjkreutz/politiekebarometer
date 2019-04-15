from pages import overview_parties
import dash_html_components as html

def get_layout():
    layout = html.Div([
        html.Div([
            html.P("""
            De politieke barometer verwerkt elk uur ongeveer 50 nieuwsartikelen en meer dan 8.000 tweets over politici 
            en politieke partijen. Dat gebeurt automatisch met behulp van een computerprogramma dat de tekst 
            taalkundig analyseert."""),
            html.P("""
            De barometer laat toe om doorheen de tijd het aantal vermeldingen te traceren van partijen, 
            politici en politieke thema's, en het sentiment van die vermeldingen (positief, negatief of neutraal). 
            Op die manier kan u de politieke "buzz" op twitter en online nieuws opvolgen."""),
            html.P([
                """Heeft u vragen of opmerking over de Politieke Barometer? Stuur ons een email (""",
                html.A("nwsdata@uantwerpen.be", href='mailto:nwsdata@uantwerpen.be'),
                ")."
            ]),
        ], className='intro-text'),
        overview_parties.get_layout(),
    ])

    return layout
