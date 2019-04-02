OVERVIEW_PARTIES = """
SELECT  mentions.id AS mentions_id, 
        pol_parties.pol_id AS pol_id, 
        fragments.id AS fragment_id, 
        doc_all.id AS doc_id,
        doc_news.news_id, 
        doc_tweets.tweet_id, 
        pol_all.color,
        pol_all.picture,
        pol_parties.short_name, 
        doc_all.ts
FROM    mentions
        JOIN pol_all
            ON mentions.pol_id=pol_all.id
        JOIN pol_parties 
            ON mentions.pol_id=pol_parties.pol_id 
        JOIN fragments 
            ON mentions.fragment_id=fragments.id 
        JOIN doc_all 
            ON fragments.doc_id=doc_all.id 
        LEFT JOIN doc_news 
            ON fragments.doc_id=doc_news.doc_id 
        LEFT JOIN doc_tweets 
            ON fragments.doc_id=doc_tweets.doc_id
WHERE   doc_all.ts BETWEEN (NOW() - INTERVAL 30 DAY) AND NOW();
"""

OVERVIEW_POLITICIANS = """
SELECT  mentions.id AS mentions_id, 
        pol_persons.pol_id AS pol_id, 
        fragments.id AS fragment_id, 
        doc_all.id AS doc_id,
        doc_news.news_id, 
        doc_tweets.tweet_id, 
        pol_all.color,
        pol_all.picture,
        pol_persons.full_name, 
        doc_all.ts
FROM    mentions
        JOIN pol_all
            ON mentions.pol_id=pol_all.id
        JOIN pol_persons 
            ON mentions.pol_id=pol_persons.pol_id 
        JOIN fragments 
            ON mentions.fragment_id=fragments.id 
        JOIN doc_all 
            ON fragments.doc_id=doc_all.id 
        LEFT JOIN doc_news 
            ON fragments.doc_id=doc_news.doc_id 
        LEFT JOIN doc_tweets 
            ON fragments.doc_id=doc_tweets.doc_id
WHERE   doc_all.ts BETWEEN (NOW() - INTERVAL 30 DAY) AND NOW();
"""

PROFILE_PARTY = """
SELECT  mentions.id AS mentions_id, 
        pol_parties.pol_id AS pol_id, 
        fragments.id AS fragment_id,
        themes.name AS theme_name,
        doc_all.id AS doc_id,
        doc_all.ts,
        doc_news.news_id, 
        doc_tweets.tweet_id, 
        pol_all.color,
        pol_all.picture,
        pol_all.info,
        pol_parties.short_name, 
        pol_parties.full_name
FROM    mentions
        JOIN pol_all
            ON mentions.pol_id=pol_all.id
        JOIN pol_parties 
            ON mentions.pol_id=pol_parties.pol_id 
        JOIN fragments 
            ON mentions.fragment_id=fragments.id 
        JOIN doc_all 
            ON fragments.doc_id=doc_all.id 
        LEFT JOIN themes
            ON doc_all.theme_code = themes.code
        LEFT JOIN doc_news 
            ON fragments.doc_id=doc_news.doc_id 
        LEFT JOIN doc_tweets 
            ON fragments.doc_id=doc_tweets.doc_id
WHERE   doc_all.ts BETWEEN (NOW() - INTERVAL 30 DAY) AND NOW() AND pol_parties.short_name=%s;
"""

PROFILE_POLITICIAN = """
SELECT  mentions.id AS mentions_id, 
        pol_persons.pol_id AS pol_id, 
        fragments.id AS fragment_id, 
        themes.name AS theme_name,
        doc_all.id AS doc_id,
        doc_news.news_id, 
        doc_tweets.tweet_id, 
        pol_all.color,
        pol_all.picture,
        pol_all.info,
        pol_persons.first_name,
        pol_persons.last_name,
        pol_persons.full_name,
        doc_all.ts
FROM    mentions
        JOIN pol_all
            ON mentions.pol_id=pol_all.id
        JOIN pol_persons 
            ON mentions.pol_id=pol_persons.pol_id 
        JOIN fragments 
            ON mentions.fragment_id=fragments.id 
        JOIN doc_all 
            ON fragments.doc_id=doc_all.id 
        LEFT JOIN themes
            ON doc_all.theme_code = themes.code
        LEFT JOIN doc_news 
            ON fragments.doc_id=doc_news.doc_id 
        LEFT JOIN doc_tweets 
            ON fragments.doc_id=doc_tweets.doc_id
WHERE   doc_all.ts BETWEEN (NOW() - INTERVAL 30 DAY) AND NOW() AND pol_persons.full_name=%s;
"""