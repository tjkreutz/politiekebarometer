PARTY_DATA = """
SELECT  mentions.id AS mentions_id,
        pol_all.id AS pol_id,
        pol_parties.short_name name,
        pol_all.color,
        pol_all.picture,
        fragments.sentiment,
        doc_all.date,
        doc_news.news_id,
        doc_tweets.tweet_id,
        themes.name AS theme_name
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
        LEFT JOIN themes
            ON doc_all.theme_code=themes.code
WHERE   doc_all.date < CURDATE() AND doc_all.date > (CURDATE() - INTERVAL 30 DAY);
"""

PARTY_POLITICIAN_DATA = """
SELECT  mentions.id AS mentions_id,
        pol_parties.pol_id AS pol_id,
        pol_parties.short_name AS name,
        pol_all.color,
        pol_all.picture,
        fragments.sentiment,
        doc_all.date,
        doc_news.news_id,
        doc_tweets.tweet_id,
        themes.name AS theme_name
FROM    mentions
        JOIN pol_persons 
            ON mentions.pol_id=pol_persons.pol_id
        JOIN pol_parties
            ON pol_persons.party_id=pol_parties.id
        JOIN pol_all
            ON pol_parties.pol_id=pol_all.id
        JOIN fragments
            ON mentions.fragment_id=fragments.id
        JOIN doc_all
            ON fragments.doc_id=doc_all.id
        LEFT JOIN doc_news
            ON fragments.doc_id=doc_news.doc_id
        LEFT JOIN doc_tweets
            ON fragments.doc_id=doc_tweets.doc_id
        LEFT JOIN themes
            ON doc_all.theme_code=themes.code
WHERE   doc_all.date < CURDATE() AND doc_all.date > (CURDATE() - INTERVAL 30 DAY);
"""

POLITICIAN_DATA = """
SELECT  mentions.id AS mentions_id,
        pol_all.id AS pol_id,
        pol_persons.full_name AS name,
        pol_all.color,
        pol_all.picture,
        pol_parties.short_name AS party_name,
        fragments.sentiment,
        doc_all.date,
        doc_news.news_id,
        doc_tweets.tweet_id,
        themes.name AS theme_name
FROM    mentions
        LEFT JOIN pol_persons 
            ON mentions.pol_id=pol_persons.pol_id
        JOIN pol_all
            ON pol_persons.pol_id=pol_all.id
        JOIN pol_parties
            ON pol_persons.party_id=pol_parties.id
        JOIN fragments
            ON mentions.fragment_id=fragments.id
        JOIN doc_all
            ON fragments.doc_id=doc_all.id
        LEFT JOIN doc_news
            ON fragments.doc_id=doc_news.doc_id
        LEFT JOIN doc_tweets
            ON fragments.doc_id=doc_tweets.doc_id
        LEFT JOIN themes
            ON doc_all.theme_code=themes.code
WHERE   doc_all.date < CURDATE() AND doc_all.date > (CURDATE() - INTERVAL 30 DAY);
"""

THEME_PROFILE = """
SELECT  *
FROM    themes
WHERE   name=%s;
"""

HASHTAGS = """
SELECT  *
FROM    hashtags
WHERE   pol_id=%s;
"""