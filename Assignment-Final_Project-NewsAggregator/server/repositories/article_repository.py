from server.db.db_connection import DBConnection
from server.models.article import Article
from server.interfaces.i_article_repository import IArticleRepository


class ArticleRepository(IArticleRepository):
    def insert_if_new(self, article: Article) -> bool:
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
