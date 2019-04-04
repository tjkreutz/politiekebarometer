from src import util

import dash_html_components as html
from app import overview_parties

def get_layout(slug):
    party_profile = util.load_party_profile(slug)
    if party_profile.empty:
        return '404. Deze pagina bestaat niet.'

    party_profile = party_profile.iloc[0]
    party_name = party_profile['short_name']
    party_picture = party_profile['picture']
    party_color = party_profile['color']
    party_full_name = party_profile['full_name']
    party_no_of_members = party_profile['no_of_members']

    df = util.select_pol_by_name(overview_parties, party_name)
    news_df = util.select_data_sources(df, ['news'])
    news_count = len(news_df.index)
    tweet_df = util.select_data_sources(df, ['twitter'])
    tweet_count = len(tweet_df.index)

    top_theme = df['theme_name'].value_counts().idxmax()

    layout = html.Div([
        html.Div([
            html.Div(html.H2('Info'), className='title-field'),
            html.Table([
                html.Tr([
                    html.Td(html.Img(src=party_picture, className='pol-picture',
                                     style={'border': f'3px solid {party_color}', 'vertical-align': 'top'})),
                    html.Td([
                        html.Tr([html.Td('Naam:'), html.Td(party_name)]),
                        html.Tr([html.Td('Volledige naam:'), html.Td(party_full_name)]),
                        html.Tr([html.Td('Aantal leden:'), html.Td(party_no_of_members)]),
                    ])
                ]),
            ])
        ], className='six columns'),
        html.Div([
            html.Div(html.H2('Data samengevat (afgelopen 30 dagen)'), className='title-field'),
            html.Table([
                html.Tr([html.Td('Aantal voorkomens in online nieuws:'), html.Td(str(news_count))]),
                html.Tr([html.Td('Aantal voorkomens op Twitter:'), html.Td(str(tweet_count))]),
                html.Tr([html.Td('Belangrijkste thema:', style={'vertical-align': 'top'}), html.Td(top_theme)]),
            ])
        ], className='six columns'),
    ], className='row')
    return layout