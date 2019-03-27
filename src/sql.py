ALL_PERSON_QUERY = """
SELECT  mentions.id AS mentions_id, 
        pol_persons.pol_id AS pol_id, 
        fragments.id AS fragment_id, 
        doc_all.id AS doc_id,
        doc_news.news_id, 
        doc_tweets.tweet_id, 
        pol_persons.first_name, 
        pol_persons.last_name, 
        pol_persons.full_name, 
        pol_persons.party_id, 
        pol_persons.info, 
        doc_all.ts, 
        doc_all.theme_code, 
        doc_all.event_name, 
        doc_all.url, 
        doc_news.source, 
        doc_tweets.username 
FROM    mentions 
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