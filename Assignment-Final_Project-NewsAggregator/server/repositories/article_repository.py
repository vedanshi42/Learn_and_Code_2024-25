from server.db.db_connection import DBConnection
from server.models.article import Article
from server.interfaces.i_article_repository import IArticleRepository
from server.services.personalization_service import PersonalizationService


class ArticleRepository(IArticleRepository):
    def insert_if_new(self, article: Article):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT article_id FROM articles
                WHERE title = %s AND source_url = %s AND date_published = %s
            """, (article.title, article.source_url, article.date_published))
            if cur.fetchone():
                return False

            cur.execute("""
                INSERT INTO articles (title, content, category_id, source_url, date_published)
                VALUES (
                    %s, %s,
                    COALESCE((SELECT category_id FROM categories WHERE name = %s),
                             (SELECT category_id FROM categories WHERE name = 'All')),
                    %s, %s
                )
            """, (article.title, article.content, article.category, article.source_url, article.date_published))
            db.commit()
            return True
        finally:
            cur.close()
            db.close()

    def insert_new_articles(self, articles: list[Article]):
        clean_articles = self.filter_ascii_articles(articles)
        for article in clean_articles:
            self.insert_if_new(article)

    def is_ascii(self, content_string: str):
        return all(ord(character) < 128 for character in content_string)

    def filter_ascii_articles(self, articles: list[Article]):
        return [
            article for article in articles
            if article.title and article.content and
            self.is_ascii(article.title) and self.is_ascii(article.content)
        ]

    def get_filtered_articles(self, filter_by=None, sort_by=None, user_id=None):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            query = """
                SELECT a.article_id, a.title, a.source_url, a.date_published,
                    COALESCE(f.likes, 0) AS likes,
                    COALESCE(f.dislikes, 0) AS dislikes,
                    c.name as category
                FROM articles a
                LEFT JOIN feedback f ON a.article_id = f.article_id
                LEFT JOIN categories c ON a.category_id = c.category_id
                WHERE (%s IS NULL OR c.name = %s OR a.date_published::text LIKE %s)
                AND a.article_id NOT IN (
                  SELECT article_id FROM user_article_feedback
                  WHERE user_id = %s AND feedback_type = 'dislike'
                )
                AND a.article_id NOT IN (
                  SELECT article_id FROM reported_articles
                  WHERE user_id = %s
                )
            """

            # sorting
            if sort_by == 'likes':
                query += " ORDER BY likes DESC"
            elif sort_by == 'dislikes':
                query += " ORDER BY dislikes DESC"
            elif sort_by == 'date_published':
                query += " ORDER BY a.date_published DESC"

            cur.execute(query, (filter_by, filter_by, f"{filter_by}%", user_id, user_id))
            rows = cur.fetchall()

            return [
                {
                    "article_id": row["article_id"],
                    "title": row["title"],
                    "source_url": row["source_url"],
                    "date_published": row["date_published"].strftime("%Y-%m-%d %H:%M:%S"),
                    "likes": row["likes"],
                    "dislikes": row["dislikes"],
                    "category": row['category']
                }
                for row in rows
            ]
        finally:
            cur.close()
            db.close()

    def get_recommended_articles(self, user_id: int):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            # Step 1: Fetch all articles (you can limit/filter further if needed)
            cur.execute("""
                SELECT a.article_id, a.title, a.content, a.source_url, a.date_published,
                    COALESCE(f.likes, 0) AS likes,
                    COALESCE(f.dislikes, 0) AS dislikes,
                    c.name AS category
                FROM articles a
                LEFT JOIN feedback f ON a.article_id = f.article_id
                JOIN categories c ON a.category_id = c.category_id
                ORDER BY a.date_published DESC
                LIMIT 100
            """)
            articles = [
                {
                    "article_id": row["article_id"],
                    "title": row["title"],
                    "content": row["content"],
                    "source_url": row["source_url"],
                    "date_published": row["date_published"].strftime("%Y-%m-%d %H:%M:%S"),
                    "likes": row["likes"],
                    "dislikes": row["dislikes"],
                    "category": row["category"]
                }
                for row in cur.fetchall()
            ]

            # Step 2: Score and return top articles
            personalization = PersonalizationService()
            scored = personalization.score_articles(user_id, articles)
            return scored[:20]
        finally:
            cur.close()
            db.close()

    def delete_article(self, user_id: int, article_id: int):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            # Step 1: Check if user is admin
            cur.execute("SELECT role FROM users WHERE user_id = %s", (user_id,))
            user = cur.fetchone()
            if not user or user["role"] != "admin":
                raise PermissionError("Only admins can delete articles.")

            # Step 2: Proceed with deletion
            cur.execute("DELETE FROM articles WHERE article_id = %s", (article_id,))
            db.commit()
            return True
        finally:
            cur.close()
            db.close()

    def get_reported_articles_with_counts(self):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT a.article_id, a.title, COUNT(r.user_id) AS report_count
                FROM reported_articles r
                JOIN articles a ON a.article_id = r.article_id
                GROUP BY a.article_id, a.title
                HAVING COUNT(r.user_id) >= 1
                ORDER BY report_count DESC
            """)
            return [{"article_id": row["article_id"], "title": row["title"], "report_count": row["report_count"]} for row in cur.fetchall()]
        finally:
            cur.close()
            db.close()
