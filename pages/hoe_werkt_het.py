import dash_html_components as html

def get_layout():
    layout = html.Div([
        html.Div(html.H2('Hoe werkt het?'), className='title-field'),
        html.P([
            """De politieke barometer verwerkt ongeveer 50 nieuwsartikelen""",
            html.Sup(html.A('1', href='#bottom')),
            """ en meer dan 8.000 tweets elk uur. Dat gebeurt automatisch met behulp van een computerprogramma dat de tekst taalkundig analyseert.""",
            html.Sup(html.A('2', href='#bottom')),
        ]),
        html.P(
            """Recente ontwikkelingen in de computertaalkunde maken het mogelijk om automatisch te bepalen waarover een tekst gaat en of het sentiment ervan eerder positief of eerder negatief is. In de politieke barometer zijn we geïnteresseerd welk sentiment er wordt uitgedrukt over politici, partijen (gemiddelde van alle politici van die partij), en de vooraf bepaalde politieke thema’s."""),
        html.P(
            """Voor het onderwerp van een tekst zoeken we naar sleutelwoorden die gebruikt worden om te communiceren over specifieke politieke thema’s als huisvesting en milieu. Om het sentiment van een tekst te bepalen kijken we naar de context waarin een politicus of thema wordt genoemd en bepalen met behulp van woordenlijsten de positieve of negatieve lading van de woorden in die context."""),
        html.P([
            """Op die manier kunnen we """,
            html.B("doorheen de tijd"),
            """ automatisch opvolgen """,
            html.B("hoe vaak"),
            """ er over specifieke politici, partijen en thema’s wordt gepraat in de pers en op Twitter (de “buzz”), en """,
            html.B("op welke manier"),
            """ (positief of negatief). We kunnen ook nagaan hoe vaak bepaalde politieke thema’s geassocieerd worden met politici en partijen. Door gebeurtenissen in de politieke actualiteit aan te duiden op de tijdlijn kunnen we ook het effect ervan op sentiment en “buzz” laten zien.""",
            ]),
        html.P(
            """De politieke barometer kan nuttig zijn voor politici, partijen, journalisten, politieke wetenschappers en iedereen met interesse voor politiek."""),
        html.P(
            """Het is evenwel belangrijk om de beperkingen van de methode te kennen. Het hele proces gebeurt automatisch en is niet perfect. Zo zit de accuraatheid van automatische taalkundige analyse van thema’s en sentiment bijvoorbeeld rond 90%. Dat betekent dat de trends correct gedetecteerd zullen zijn, maar individuele tweets en persberichten kunnen regelmatig fout geanalyseerd worden. Er is ook aangetoond in onderzoek dat sentiment in specifieke media als Twitter op zich niet voldoende informatie biedt om bijvoorbeeld de uitslag van verkiezingen te voorspellen."""),
        html.Hr(id='bottom'),
        html.P([
            """Heeft u vragen of opmerking over de Politieke Barometer? Bezoek onze projectwebsite (""",
            html.A('NWS data', href='https://www.uantwerpen.be/nl/projecten/nws-data/', target='_blank'),
            """) of stuur ons een email (""",
            html.A('nwsdata@uantwerpen.be', id='email', href='mailto:nwsdata@uantwerpen.be'),
            """).""",
        ]),
        html.P(
            """1. Het gaat hier om publiek toegankelijke artikelen van de websites van De Standaard, Het Nieuwsblad, Gazet van Antwerpen, Het Belang van Limburg, De Morgen, Het Laatste Nieuws, De Tijd, Metro, Knack, Trends, Humo, Krant van West-Vlaanderen, De Zondag en tPallieterke. """, style={'font-size': '75%'}),
        html.P([
            """2. In 2014 werd al eens hetzelfde ondernomen op de oorspronkelijke """,
            html.A('Politieke Barometer', href='http://politiekebarometer.be/', target='_blank'),
            """.""",
        ], style={'font-size': '75%'})
    ], className='page-text')

    return layout
