from src import util
from src import widgets

import dash_core_components as dcc
import dash_html_components as html

from app import party_data

def get_layout(slug):
    party_profile = util.select_pol_by_name(party_data, util.slug_to_name(slug))
    if party_profile.empty:
        return '404. Deze pagina bestaat niet.'

    party_profile = party_profile.iloc[0]
    party_name = party_profile['name']
    party_picture = party_profile['picture']
    party_color = party_profile['color']

    df = util.select_pol_by_name(party_data, party_name)
    news_df = util.select_data_sources(df, ['news'])
    news_count = len(news_df.index)
    tweet_df = util.select_data_sources(df, ['twitter'])
    tweet_count = len(tweet_df.index)

    top_theme = news_df['theme_name'].value_counts().idxmax()

    layout = html.Div([
        html.Div([
            html.Div([
                html.Div(html.H2('Info'), className='title-field'),
                html.Table([
                    html.Tr([
                        html.Td(html.Img(src=party_picture, className='pol-picture',
                                         style={'border': f'3px solid {party_color}', 'vertical-align': 'top'})),
                        html.Td([
                            html.Tr([html.Td('Naam:'), html.Td(party_name)]),
                        ])
                    ]),
                ], style={'margin': '10px 0'}),
                html.Div(html.H2("Data samengevat (laatste 30 dagen)"), className='title-field2'),
                html.Table([
                    html.Tr([html.Td('Aantal voorkomens in online nieuws:'), html.Td(str(news_count))]),
                    html.Tr([html.Td('Aantal voorkomens op Twitter:'), html.Td(str(tweet_count))]),
                    html.Tr([html.Td('Belangrijkste thema:', style={'vertical-align': 'top'}), html.Td(top_theme)]),
                ], style={'margin': '10px 0'}),
                html.Div(html.H2('Hashtags'), className='title-field2'),
                widgets.word_cloud(df, 10),
            ], className='six columns'),
            html.Div([
                html.Div(html.H2('Aantal voorkomens'), className='title-field'),
                html.Center([html.B("Figuur 1: "), html.Span("Aantal voorkomens {} in online nieuws en op Twitter".format(party_name))], className='description'),
                html.Div(widgets.double_mention_graph(news_df, tweet_df))
            ], className='six columns'),
        ], className='row'),
        html.Div([
            html.Div([
                html.Div(html.H2("Opinie op Twitter"), className='title-field'),
                html.Center([html.B("Figuur 2: "), html.Span("Evolutie opinie over {}".format(party_name))], className='description'),
                widgets.sentiment_area_graph(tweet_df)
            ], className='six columns'),
            html.Div([
                html.Div(html.H2("Thema's in het nieuws"), className='title-field'),
                html.Center([html.B("Figuur 3: "), html.Span("Distributie top 5 thema's")], className='description'),
                widgets.theme_bar_chart(news_df),
            ], className='six columns'),
        ], className='row'),
    ])
    return layout