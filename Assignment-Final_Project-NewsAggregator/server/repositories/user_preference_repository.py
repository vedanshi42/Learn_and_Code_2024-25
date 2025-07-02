from server.db.db_connection import DBConnection
from server.interfaces.i_user_preference_repository import IUserPreferenceRepository


class UserPreferenceRepository(IUserPreferenceRepository):
    def __init__(self):
        self.db = DBConnection()

    def get_liked_categories(self, user_id: int):
        cur = self.db.get_cursor()
        cur.execute("""
            SELECT c.name
            FROM user_article_feedback uaf
            JOIN articles a ON uaf.article_id = a.article_id
            JOIN categories c ON a.category_id = c.category_id
            WHERE uaf.user_id = %s
            GROUP BY c.name
            HAVING COUNT(*) FILTER (WHERE uaf.feedback_type = 'like') >
           COUNT(*) FILTER (WHERE uaf.feedback_type = 'dislike')
        """, (user_id,))
        result = {row["name"] for row in cur.fetchall()}
        cur.close()
        return result

    def get_enabled_keywords(self, user_id: int):
        cur = self.db.get_cursor()
        cur.execute("""
            SELECT keyword FROM keywords
            WHERE user_id = %s AND is_enabled = TRUE
        """, (user_id,))
        result = [row["keyword"].lower() for row in cur.fetchall()]
        cur.close()
        return result

    def get_disliked_keywords_and_urls(self, user_id: int):
        cur = self.db.get_cursor()
        cur.execute("""
            SELECT LOWER(a.title) AS title, LOWER(COALESCE(a.content, '')) AS content,
                   LOWER(a.source_url) as url
            FROM user_article_feedback f
            JOIN articles a ON a.article_id = f.article_id
            WHERE (f.user_id = %s AND f.feedback_type = 'dislike')
               OR a.article_id IN (SELECT article_id FROM reported_articles WHERE user_id = %s)
        """, (user_id, user_id))
        disliked_titles, disliked_contents, disliked_urls = [], [], []

        for row in cur.fetchall():
            disliked_titles.extend(row['title'].split())
            disliked_contents.extend(row['content'].split())
            disliked_urls.append(row['url'])

        cur.close()
        disliked_keywords = set(kw for kw in (disliked_titles + disliked_contents) if len(kw) > 3)
        return disliked_keywords, disliked_urls
