from server.db.db_connection import DBConnection


class SearchArticleRepository():
    def find_articles_by_category_or_keyword(self, category=None, keyword=None):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            query = """
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
            """
            category_pattern = ''
            keyword_pattern = ''

            if category:
                category_pattern = f'%{category}%'
            elif keyword:
                keyword_pattern = f'%{keyword}%'

            cur.execute(query, (category_pattern, keyword_pattern, keyword_pattern))
            return cur.fetchall()
        finally:
            cur.close()
            db.close()

    def find_today_articles(self):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT DISTINCT article_id, title, source_url, date_published FROM articles
                WHERE date_published::date = CURRENT_DATE
                ORDER BY date_published DESC
            """)
            return {row['article_id']: [row['title'], row['source_url'], row['date_published'].strftime("%Y-%m-%d %H:%M:%S")] for row in cur.fetchall()}
        finally:
            cur.close()
            db.close()

    def find_by_date_range(self, from_date, to_date):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT DISTINCT article_id, title, source_url, date_published FROM articles
                WHERE date_published BETWEEN %s AND %s
                ORDER BY date_published DESC
            """, (from_date, to_date))
            return {row['article_id']: [row['title'], row['source_url'], row['date_published'].strftime("%Y-%m-%d %H:%M:%S")] for row in cur.fetchall()}
        finally:
            cur.close()
            db.close()

    def search_by_keyword(self, keyword):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            pattern = f"%{keyword}%"
            cur.execute("""
                SELECT DISTINCT article_id, title, source_url, date_published FROM articles
                WHERE title ILIKE %s OR content ILIKE %s
                ORDER BY date_published DESC
            """, (pattern, pattern))
            return {row['article_id']: [row['title'], row['source_url'], row['date_published'].strftime("%Y-%m-%d %H:%M:%S")] for row in cur.fetchall()}
        finally:
            cur.close()
            db.close()

    def search_by_category(self, category):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT DISTINCT article_id, title, source_url, date_published FROM articles
                WHERE category_id = (
                    SELECT category_id FROM categories WHERE name = %s
                )
                ORDER BY date_published DESC
            """, (category,))
            return {row['article_id']: [row['title'], row['source_url'], row['date_published'].strftime("%Y-%m-%d %H:%M:%S")] for row in cur.fetchall()}
        finally:
            cur.close()
            db.close()

    def search_by_date(self, date):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT DISTINCT article_id, title, date_published FROM articles
                WHERE date_published = %s
                ORDER BY date_published DESC
            """, (date,))
            return {row['article_id']: [row['title'], row['date_published'].strftime("%Y-%m-%d %H:%M:%S")] for row in cur.fetchall()}
        finally:
            cur.close()
            db.close()
