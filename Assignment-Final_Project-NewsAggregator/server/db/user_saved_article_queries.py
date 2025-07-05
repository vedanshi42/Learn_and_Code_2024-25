# SQL queries for UserSavedArticleRepository

SAVE_BY_ID = '''
    INSERT INTO user_saved_articles (user_id, article_id, title, content, category, source_url, date_published)
    SELECT %s, article_id, title, content, c.name, source_url, date_published
    FROM articles a
    JOIN categories c ON a.category_id = c.category_id
    WHERE a.article_id = %s
    ON CONFLICT DO NOTHING
'''

DELETE_BY_ID = '''
    DELETE FROM user_saved_articles
    WHERE article_id = %s AND user_id = %s
'''

GET_SAVED_ARTICLES = '''
    SELECT DISTINCT article_id, title, content, source_url, date_published
    FROM user_saved_articles
    WHERE user_id = %s
    ORDER BY date_published DESC
'''
