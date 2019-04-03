from pages import overview_parties
import dash_html_components as html

# define layout
layout = html.Div([
    html.Div([
        html.P("""
        De politieke barometer verwerkt ongeveer 1.000 nieuwsartikelen en meer dan 200.000 tweets over politici 
        en politieke partijen per dag. Dat gebeurt automatisch met behulp van een computerprogramma dat de tekst 
        taalkundig analyseert."""),
    ], className='intro-text'),
    overview_parties.layout,
])
