from src import util
from src import widgets

import dash_html_components as html

from app import party_data

def get_layout(slug):
    theme_profile = util.load_theme_profile(util.slug_to_name(slug))
    if theme_profile.empty:
        return '404. Deze pagina bestaat niet.'

    theme_profile = theme_profile.iloc[0]
    theme_name = theme_profile['name']
    theme_info = theme_profile['info']

    df = util.select_by_theme(party_data, theme_name)
    tweet_df = util.select_data_sources(df, ['twitter'])
    news_party_df = util.select_data_sources(party_data, ['news'])

    layout = html.Div([
        html.Div([
            html.Div(html.H2('Info'), className='title-field'),
            html.Table([
                html.Tr([
                    html.Td([
                        html.Tr([html.Td('Naam:'), html.Td(html.B(theme_name))]),
                        html.Tr([html.Td('Info:', style={'vertical-align': 'top'}), html.Td(theme_info)]),
                    ])
                ]),
            ], style={'margin': '10px 0'}),
        ]),
        html.Div([
            html.Div([
                html.H2('Partijen in het nieuws', className='title-field'),
                html.Center([html.B("Figuur 1: "), html.Span("Partijen waarbij nieuws relatief vaak gaat over dit thema")], className='description'),
                widgets.party_bar_chart(news_party_df, theme_name),
            ], className='six columns'),
            html.Div([
                html.H2('Opinie op Twitter over dit thema', className='title-field'),
                html.Center([html.B("Figuur 2: "), html.Span("Evolutie opinie")], className='description'),
                widgets.sentiment_area_graph(tweet_df)
            ], className='six columns')
        ], className='row')
    ])

    return layout