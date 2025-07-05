# SQL queries for UserPreferenceRepository

GET_LIKED_CATEGORIES = '''
    SELECT DISTINCT c.name
    FROM user_article_feedback uaf
    JOIN articles a ON uaf.article_id = a.article_id
    JOIN categories c ON a.category_id = c.category_id
    WHERE uaf.user_id = %s
    GROUP BY c.name
    HAVING COUNT(*) FILTER (WHERE uaf.feedback_type = 'like') >
           COUNT(*) FILTER (WHERE uaf.feedback_type = 'dislike')
'''

GET_DISLIKED_CATEGORIES = '''
    SELECT DISTINCT c.name
    FROM user_article_feedback uaf
    JOIN articles a ON uaf.article_id = a.article_id
    JOIN categories c ON a.category_id = c.category_id
    WHERE uaf.user_id = %s
    GROUP BY c.name
    HAVING COUNT(*) FILTER (WHERE uaf.feedback_type = 'dislike') >
           COUNT(*) FILTER (WHERE uaf.feedback_type = 'like')
'''

GET_ENABLED_KEYWORDS = '''
    SELECT DISTINCT keyword FROM keywords
    WHERE user_id = %s AND is_enabled = TRUE
'''

GET_DISLIKED_KEYWORDS = '''
    SELECT DISTINCT LOWER(a.title) AS title, LOWER(COALESCE(a.content, '')) AS content,
           LOWER(a.source_url) as url
    FROM user_article_feedback f
    JOIN articles a ON a.article_id = f.article_id
    WHERE (f.user_id = %s AND f.feedback_type = 'dislike')
       OR a.article_id IN (SELECT article_id FROM reported_articles WHERE user_id = %s)
'''

GET_LIKED_KEYWORDS = '''
    SELECT DISTINCT LOWER(a.title) AS title, LOWER(COALESCE(a.content, '')) AS content,
           LOWER(a.source_url) as url
    FROM user_article_feedback f
    JOIN articles a ON a.article_id = f.article_id
    WHERE f.user_id = %s AND f.feedback_type = 'like'
'''

GET_SAVED_ARTICLE_CATEGORIES = '''
    SELECT DISTINCT c.name
    FROM saved_articles sa
    JOIN articles a ON sa.article_id = a.article_id
    JOIN categories c ON a.category_id = c.category_id
    WHERE sa.user_id = %s
'''

GET_SAVED_ARTICLE_KEYWORDS = '''
    SELECT DISTINCT LOWER(a.title) AS title, LOWER(COALESCE(a.content, '')) AS content,
           LOWER(a.source_url) as url
    FROM saved_articles sa
    JOIN articles a ON sa.article_id = a.article_id
    WHERE sa.user_id = %s
'''
