
import psycopg2
from psycopg2.extras import RealDictCursor
from server.models.article import Article
from server.services.ml_category_predictor import MLCategoryPredictor


class ArticleRecategorizer:
    def __init__(self):
        self.db = self._connect_db()
        self.predictor = MLCategoryPredictor()

    def _connect_db(self):
        return psycopg2.connect(
            dbname="news_aggregator_db",
            user="news_agg_user",
            password="newsagg123",  # 🔁 update this
            host="localhost",
            port="5432"
        )

    def _get_all_articles(self):
        with self.db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT article_id, title, content, source_url, date_published
                FROM articles
            """)
            rows = cur.fetchall()
            articles = []
            for row in rows:
                article = Article(
                    title=row["title"],
                    content=row["content"],
                    source_url=row["source_url"],
                    date_published=row["date_published"],
                    category="All"  # or dummy value; will be overwritten by ML
                )
                setattr(article, "article_id", row["article_id"])
                articles.append(article)
            return articles

    def _add_category_if_not_exists(self, category_name: str):
        with self.db.cursor() as cur:
            cur.execute("SELECT category_id FROM categories WHERE name = %s", (category_name,))
            if not cur.fetchone():
                cur.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
        self.db.commit()

    def _update_article_category(self, article_id: int, category_name: str):
        with self.db.cursor() as cur:
            cur.execute("""
                UPDATE articles
                SET category_id = (
                    SELECT category_id FROM categories WHERE name = %s
                )
                WHERE article_id = %s
            """, (category_name, article_id))
        self.db.commit()

    def recategorize_all(self):
        articles = self._get_all_articles()
        print(f"🔍 Found {len(articles)} articles to re-categorize.\n")

        updated = 0
        for article in articles:
            new_category = self.predictor.predict(article)
            self._add_category_if_not_exists(new_category)
            self._update_article_category(article.article_id, new_category)

            print(f"✅ Article ID {article.article_id} → {new_category}")
            updated += 1

        print(f"\n🎉 Done. {updated} articles updated.")


if __name__ == "__main__":
    recategorizer = ArticleRecategorizer()
    recategorizer.recategorize_all()
