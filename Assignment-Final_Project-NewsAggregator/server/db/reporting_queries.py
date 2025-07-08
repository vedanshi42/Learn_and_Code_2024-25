# SQL queries for Reporting Repository

REPORT_ARTICLE = '''
    INSERT INTO reported_articles (user_id, article_id)
    VALUES (%s, %s) ON CONFLICT DO NOTHING
'''
