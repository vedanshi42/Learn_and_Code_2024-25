# SQL queries for ArticleRepository

INSERT_IF_NEW = '''
    SELECT article_id FROM articles
    WHERE title = %s AND source_url = %s AND date_published = %s
'''

INSERT_ARTICLE = '''
    INSERT INTO articles (title, content, category_id, source_url, date_published)
    VALUES (
        %s, %s,
        COALESCE((SELECT category_id FROM categories WHERE name = %s),
                 (SELECT category_id FROM categories WHERE name = 'All')),
        %s, %s
    )
'''

GET_FILTERED_ARTICLES = '''
    SELECT a.article_id, a.title, a.source_url, a.date_published,
        COALESCE(f.likes, 0) AS likes,
        COALESCE(f.dislikes, 0) AS dislikes,
        c.name as category
    FROM articles a
    LEFT JOIN feedback f ON a.article_id = f.article_id
    LEFT JOIN categories c ON a.category_id = c.category_id
    WHERE (%s IS NULL OR c.name = %s OR a.date_published::text LIKE %s)
    AND (c.is_enabled_by_admin IS TRUE)
    AND (
        NOT EXISTS (
            SELECT 1 FROM keywords k
            WHERE k.is_enabled_by_admin = FALSE
              AND k.keyword IN (
                  SELECT regexp_split_to_table(a.title || ' ' || a.content, '\\s+')
              )
        )
    )
    AND a.article_id NOT IN (
      SELECT article_id FROM user_article_feedback
      WHERE user_id = %s AND feedback_type = 'dislike'
    )
    AND a.article_id NOT IN (
      SELECT article_id FROM reported_articles
      WHERE user_id = %s
    )
'''

GET_RECOMMENDED_ARTICLES = '''
    SELECT a.article_id, a.title, a.content, a.source_url, a.date_published,
        COALESCE(f.likes, 0) AS likes,
        COALESCE(f.dislikes, 0) AS dislikes,
        c.name AS category
    FROM articles a
    LEFT JOIN feedback f ON a.article_id = f.article_id
    JOIN categories c ON a.category_id = c.category_id
    WHERE
        c.is_enabled_by_admin IS TRUE
        AND (
            NOT EXISTS (
                SELECT 1 FROM keywords k
                WHERE k.is_enabled_by_admin = FALSE
                  AND k.keyword IN (
                      SELECT regexp_split_to_table(a.title || ' ' || a.content, '\\s+')
                  )
            )
        )
    ORDER BY a.date_published DESC
    LIMIT 100
'''

CHECK_ADMIN = 'SELECT role FROM users WHERE user_id = %s'
DELETE_ARTICLE = 'DELETE FROM articles WHERE article_id = %s'

GET_REPORTED_ARTICLES = '''
    SELECT a.article_id, a.title, COUNT(r.user_id) AS report_count
    FROM reported_articles r
    JOIN articles a ON a.article_id = r.article_id
    GROUP BY a.article_id, a.title
    HAVING COUNT(r.user_id) >= 1
    ORDER BY report_count DESC
'''
