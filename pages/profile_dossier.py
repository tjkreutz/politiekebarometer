from src import util, widgets
from app import party_data, politician_data

import dash_core_components as dcc
import dash_html_components as html

def get_layout(slug):
    dossier_name = util.slug_to_name(slug)
    dossier_descriptions = widgets.dossier_definitions()

    if not dossier_name in dossier_descriptions:
        return '404. Deze pagina bestaat niet.'

    dossier_picture = dossier_descriptions[dossier_name]['picture']
    dossier_extended_info = dossier_descriptions[dossier_name]['extended_info']

    party_df = party_data.loc[party_data['dossier_name'] == dossier_name]
    politician_df = politician_data.loc[politician_data['dossier_name'] == dossier_name]

    news_df = util.select_data_sources(party_df, ['news'])
    news_count = len(news_df.index)
    tweet_df = util.select_data_sources(party_df, ['twitter'])
    tweet_count = len(tweet_df.index)

    layout = html.Div([
        html.Div([
            html.Div([
                html.Div(html.H2(dossier_name), className='title-field'),
                html.Img(src=dossier_picture, className='dossier-picture'),
                dossier_extended_info,
                html.Div(html.H2("Data samengevat (laatste 30 dagen)"), className='title-field2'),
                html.Table([
                    html.Tr([html.Td('Aantal voorkomens in online nieuws:'), html.Td(str(news_count))]),
                    html.Tr([html.Td('Aantal voorkomens op Twitter:'), html.Td(str(tweet_count))]),
                ], style={'margin': '28px 0'}),
                html.Div([
                    html.Div(html.H2('Aantal voorkomens'), className='title-field'),
                    html.Center([html.B("Figuur 1: "),
                                 html.Span("Aantal voorkomens {} in online nieuws en op Twitter".format(dossier_name))],
                                className='description'),
                    html.Div(widgets.double_mention_graph_small(news_df, tweet_df))
                ]),
            ], className='six columns'),
            html.Div([
                html.Div(html.H2('Partijen en politici'), className='title-field'),
                html.P("""
                Welke partijen en politici komen het vaakst voor in berichten over dit dossier? We tellen alle
                voorkomens van partijen en politici in tweets en nieuwsberichten die {} vermelden, en delen ze door
                het totaal aantal berichten over het dossier.""".format(dossier_name,), {'margin-top': '10px'}),
                html.Div([
                    html.Div(html.H2('Partijen'), className='title-field2'),
                    html.Center([
                        html.B("Figuur 2: "),
                        html.Span("Welke partijen komen het vaakst voor met {}?".format(dossier_name))
                    ], className='description'),
                    widgets.pol_bar_chart(party_df),
                ]),
                html.Div([
                    html.Div(html.H2('Politici'), className='title-field2'),
                    html.Center([
                        html.B("Figuur 3: "),
                        html.Span("Welke politici komen het vaakst voor met {}?".format(dossier_name))
                    ], className='description'),
                    widgets.pol_bar_chart(politician_df),
                ]),
            ], className='six columns'),
        ], className='row'),
        html.Div([
            html.Div(html.H2('Opinie op Twitter over {}'.format(dossier_name)), className='title-field'),
            html.Center([
                html.B("Figuur 4: "),
                html.Span("Evolutie opinie")
            ], className='description'),
            widgets.sentiment_area_graph(tweet_df)
        ], className='row')
    ])

    return layout
