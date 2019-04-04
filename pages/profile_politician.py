from src import util

import dash_html_components as html
from app import overview_politicians

def get_layout(slug):
    politician_profile = util.load_politician_profile(slug)
    if politician_profile.empty:
        return '404. Deze pagina bestaat niet.'

    politician_profile = politician_profile.iloc[0]
    politician_name = politician_profile['full_name']
    politician_picture = politician_profile['picture']
    politician_color = politician_profile['color']
    politician_party = politician_profile['party_name']

    df = util.select_pol_by_name(overview_politicians, politician_name)
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
                    html.Td(html.Img(src=politician_picture, className='pol-picture',
                                     style={'border': f'3px solid {politician_color}', 'vertical-align': 'top'})),
                    html.Td([
                        html.Tr([html.Td('Naam:'), html.Td(politician_name)]),
                        html.Tr([html.Td('Partij:'), html.Td(politician_party)])
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