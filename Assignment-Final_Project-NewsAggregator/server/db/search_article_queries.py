# SQL queries for SearchArticleRepository

SEARCH_ARTICLES = '''
    SELECT * FROM articles
    WHERE title ILIKE %s OR content ILIKE %s
    ORDER BY date_published DESC
'''

FIND_ARTICLES_BY_CATEGORY_OR_KEYWORD = '''
    SELECT DISTINCT a.article_id, a.title, a.source_url, a.date_published
    FROM articles a
    LEFT JOIN categories c ON a.category_id = c.category_id
    WHERE
        c.name LIKE %s OR
        (
            a.title ILIKE %s OR
            a.content ILIKE %s
        )
    ORDER BY a.date_published DESC
'''


SEARCH_BY_KEYWORD = '''
    SELECT DISTINCT article_id, title, source_url, date_published FROM articles
    WHERE title ILIKE %s OR content ILIKE %s
    ORDER BY date_published DESC
'''

SEARCH_BY_CATEGORY = '''
    SELECT DISTINCT article_id, title, source_url, date_published FROM articles
    WHERE category_id = (
        SELECT category_id FROM categories WHERE name = %s
    )
    ORDER BY date_published DESC
'''

SEARCH_BY_DATE = '''
    SELECT DISTINCT article_id, title, date_published FROM articles
    WHERE date_published = %s
    ORDER BY date_published DESC
'''
