from src import util
from src import widgets

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
        html.Div(
            html.Div([
                html.Div(widgets.breadcrumbs('breadcrumbs'), className='eight columns'),
                html.Div(className='four columns'),
            ], className='row'),
            className='search-container'),
        html.Div([
            html.Div([
                html.Div(html.H2('Info'), className='title-field'),
                html.Table([
                    html.Tr([
                        html.Td(html.Img(src=politician_picture, className='pol-picture',
                                         style={'border': f'3px solid {politician_color}', 'vertical-align': 'top'})),
                        html.Td([
                            html.Tr([html.Td('Naam:'), html.Td(politician_name)]),
                            html.Tr([html.Td('Partij:'), html.Td(html.A(politician_party, href='/partijen/{}'.format(
                                util.name_to_slug(politician_party))))])
                        ])
                    ]),
                ], style={'margin': '10px 0'}),
                html.Div(html.H2('Data samengevat (afgelopen 30 dagen)'), className='title-field2'),
                html.Table([
                    html.Tr([html.Td('Aantal voorkomens in online nieuws:'), html.Td(str(news_count))]),
                    html.Tr([html.Td('Aantal voorkomens op Twitter:'), html.Td(str(tweet_count))]),
                    html.Tr([html.Td('Belangrijkste thema:', style={'vertical-align': 'top'}),
                             html.Td(html.A(top_theme, href='/themas/{}'.format(util.name_to_slug(top_theme))))]),
                ], style={'margin': '10px 0'}),
                html.Div(html.H2('Kernwoorden'), className='title-field2'),
                widgets.word_cloud(df, 10),
            ], className='six columns'),
            html.Div([
                html.Div(html.H2('Aantal voorkomens'), className='title-field'),
                html.Center([html.B("Figuur 1: "), html.Span("Aantal voorkomens {} in online nieuws en op Twitter".format(politician_name))], className='description'),
                html.Div(widgets.double_mention_graph(news_df, tweet_df))
            ], className='six columns'),
        ], className='row'),
        html.Div([
            html.Div([
                html.Div(html.H2("Top thema's"), className='title-field'),
                html.Center([html.B("Figuur 4: "), html.Span("Distributie top 5 thema's")], className='description'),
                widgets.theme_bar_chart(df),
            ], className='five columns'),
            html.Div([
                html.Div(html.H2("Opinie op Twitter (laatste 30 dagen)"), className='title-field'),
                html.Div([
                    html.Div([
                        html.Center([html.B("Figuur 2: "), html.Span("Distributie opinie")], className='description'),
                        widgets.sentiment_donut(df),
                    ], className='five columns'),
                    html.Div([
                        html.Center([html.B("Figuur 3: "), html.Span("Evolutie opinie")], className='description'),
                        widgets.sentiment_graph(df)
                    ], className='seven columns')
                ], className='row')
            ], className='seven columns'),
        ], className='row'),
    ])

    return layout