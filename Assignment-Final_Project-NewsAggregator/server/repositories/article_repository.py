from contextlib import contextmanager
from server.db.db_connection import DBConnection
from server.models.article import Article
from server.interfaces.i_article_repository import IArticleRepository
from server.db.article_queries import (
    INSERT_IF_NEW, INSERT_ARTICLE, GET_FILTERED_ARTICLES, GET_RECOMMENDED_ARTICLES,
    CHECK_ADMIN, DELETE_ARTICLE, GET_REPORTED_ARTICLES
)
from server.exceptions.repository_exception import (
    NotFoundException, DuplicateEntityException,
    PermissionDeniedException, RepositoryException
)
from server.config.logging_config import news_agg_logger


@contextmanager
def get_db_cursor():
    db = DBConnection()
    cur = db.get_cursor()
    try:
        yield cur, db
    finally:
        cur.close()
        db.close()


class ArticleRepository(IArticleRepository):
    def insert_if_new(self, article: Article):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(INSERT_IF_NEW, (article.title, article.source_url, article.date_published))

                if cur.fetchone():
                    return False

                cur.execute(INSERT_ARTICLE, (article.title, article.content, article.category, article.source_url, article.date_published))
                db.commit()
                news_agg_logger(20, f"Inserted new article: {article.title}")
                return True

        except Exception as e:
            with get_db_cursor() as (cur, db):
                db.rollback()
            news_agg_logger(40, f"Failed to insert article: {e}")
            raise RepositoryException(f"Failed to insert article: {e}")

    def insert_new_articles(self, articles: list[Article]):
        clean_articles = self.filter_ascii_articles(articles)
        for article in clean_articles:
            try:
                self.insert_if_new(article)
            except DuplicateEntityException:
                news_agg_logger(20, f"Duplicate article skipped in batch: {article.title}")
                continue

    def is_ascii(self, content_string: str):
        return all(ord(character) < 128 for character in content_string)

    def filter_ascii_articles(self, articles: list[Article]):
        return [
            article for article in articles
            if article.title and article.content and
            self.is_ascii(article.title) and self.is_ascii(article.content)
        ]

    def get_filtered_articles(self, filter_by=None, sort_by=None, user_id=None):
        try:
            with get_db_cursor() as (cur, db):
                query = GET_FILTERED_ARTICLES

                if sort_by == 'likes':
                    query += " ORDER BY likes DESC"
                elif sort_by == 'dislikes':
                    query += " ORDER BY dislikes DESC"
                elif sort_by == 'date_published':
                    query += " ORDER BY a.date_published DESC"

                cur.execute(query, (filter_by, filter_by, f"{filter_by}%", user_id, user_id))
                rows = cur.fetchall()

                if not rows:
                    news_agg_logger(30, "No articles found for filter.")
                    raise NotFoundException("No articles found.")

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

        except NotFoundException:
            raise
        except Exception as e:
            news_agg_logger(40, f"Failed to fetch filtered articles: {e}")
            raise RepositoryException(f"Failed to fetch filtered articles: {e}")

    def get_recommended_articles(self, user_id: int):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_RECOMMENDED_ARTICLES)

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

                if not articles:
                    news_agg_logger(30, f"No recommended articles found for user {user_id}.")
                    raise NotFoundException("No recommended articles found.")

                news_agg_logger(20, f"Getting recommended articles for user {user_id}.")
                return articles
        except NotFoundException:
            raise
        except Exception as e:
            news_agg_logger(40, f"Failed to fetch recommended articles: {e}")
            raise RepositoryException(f"Failed to fetch recommended articles: {e}")

    def delete_article(self, user_id: int, article_id: int):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(CHECK_ADMIN, (user_id,))
                user = cur.fetchone()

                if not user or user["role"] != "admin":
                    news_agg_logger(30, f"Permission denied for user {user_id} to delete article {article_id}.")
                    raise PermissionDeniedException("Only admins can delete articles.")

                cur.execute(DELETE_ARTICLE, (article_id,))
                db.commit()

                news_agg_logger(20, f"Article {article_id} deleted by admin {user_id}.")
                return True
        except PermissionDeniedException:
            raise
        except Exception as e:
            with get_db_cursor() as (cur, db):
                db.rollback()
            news_agg_logger(40, f"Failed to delete article: {e}")
            raise RepositoryException(f"Failed to delete article: {e}")

    def get_reported_articles_with_counts(self):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_REPORTED_ARTICLES)
                rows = cur.fetchall()

                if not rows:
                    news_agg_logger(30, "No reported articles found.")

                return [{"article_id": row["article_id"], "title": row["title"], "report_count": row["report_count"]} for row in rows]

        except Exception as e:
            news_agg_logger(40, f"Failed to fetch reported articles: {e}")
            raise RepositoryException(f"Failed to fetch reported articles: {e}")
