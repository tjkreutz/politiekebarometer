from src import util

import dash_html_components as html

def get_layout(slug):
    # load data
    df = util.load_party(slug)
    if df.empty:
        return '404. Deze pagina bestaat niet.'

    # define layout
    layout = html.Div((html.P(df['short_name'].iloc[0])))
    return layout