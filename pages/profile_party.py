from src import util
from src import widgets

from random import randrange
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
                ], style={'margin': '10px 0'}),
                html.Div(html.H2('Data samengevat (afgelopen 30 dagen)'), className='title-field2'),
                html.Table([
                    html.Tr([html.Td('Aantal voorkomens in online nieuws:'), html.Td(str(news_count))]),
                    html.Tr([html.Td('Aantal voorkomens op Twitter:'), html.Td(str(tweet_count))]),
                    html.Tr([html.Td('Belangrijkste thema:', style={'vertical-align': 'top'}), html.Td(html.A(top_theme, href='/themas/{}'.format(util.name_to_slug(top_theme))))]),
                ], style={'margin': '10px 0'}),
                html.Div(html.H2('Kernwoorden'), className='title-field2'),
                widgets.word_cloud(df, 10),
            ], className='six columns'),
            html.Div([
                html.Div(html.H2('Aantal voorkomens'), className='title-field'),
                html.Center(html.P([html.B("Figuur 1: "), html.Span(
                    "Aantal voorkomens {} in online nieuws en op Twitter".format(party_name))],
                                   style={'font-size': '75%'})),
                html.Div(widgets.double_mention_graph(news_df, tweet_df))
            ], className='six columns'),
        ], className='row'),
        html.Div([
            html.Div([
                html.Div(html.H2("Top thema's"), className='title-field'),
                html.Center(html.P([html.B("Figuur 4: "), html.Span(
                    "Distributie top 5 thema's")], style={'font-size': '75%'})),
                widgets.theme_bar_chart(df),
            ], className='five columns'),
            html.Div([
                html.Div(html.H2("Opinie op Twitter (laatste 30 dagen)"), className='title-field'),
                html.Div([
                    html.Div([
                        html.Center(html.P([html.B("Figuur 2: "), html.Span(
                            "Distributie opinie")],style={'font-size': '75%'})),
                        widgets.sentiment_donut(df),
                    ], className='five columns'),
                    html.Div([
                        html.Center(html.P([html.B("Figuur 3: "), html.Span(
                            "Evolutie opinie")], style={'font-size': '75%'})),
                        widgets.sentiment_graph(df)
                    ], className='seven columns')
                ], className='row')
            ], className='seven columns'),
        ], className='row'),
    ])
    return layout