from src import util

import dash_html_components as html

def get_layout(slug):
    # load data
    df = util.load_politician(slug)
    if df.empty:
        return '404. Deze pagina bestaat niet.'

    politician_name = df['full_name'].iloc[0]
    politician_picture = df['picture'].iloc[0]
    politician_color = df['color'].iloc[0]
    politician_party = df['party_name'].iloc[0]

    news_df = df.loc[df['news_id'].notnull()]
    news_count = len(news_df.index)
    tweet_df = df.loc[df['tweet_id'].notnull()]
    tweet_count = len(tweet_df.index)

    top_theme = df['theme_name'].value_counts().idxmax()

    # define layout
    layout = html.Div([
        html.Div([
            html.Div(html.H2('Info'), className='title-field'),
            html.Table([
                html.Tr([
                    html.Td(html.Img(src=politician_picture, className='politician-picture',
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