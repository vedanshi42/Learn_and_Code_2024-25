from server.db.db_connection import DBConnection


class PersonalizationService:
    def __init__(self):
        self.db = DBConnection()

    def score_articles(self, user_id: int, articles: list[dict]) -> list[dict]:
        cur = self.db.get_cursor()

        # 1. Get liked category preferences
        cur.execute("""
            SELECT c.name FROM feedback f
            JOIN articles a ON a.article_id = f.article_id
            JOIN categories c ON a.category_id = c.category_id
            WHERE f.user_id = %s AND f.likes > f.dislikes
            GROUP BY c.name ORDER BY COUNT(*) DESC LIMIT 3
        """, (user_id,))
        preferred_cats = {row['name'] for row in cur.fetchall()}

        # 2. Get enabled keywords
        cur.execute("""
            SELECT keyword FROM keywords
            WHERE user_id = %s AND is_enabled = TRUE
        """, (user_id,))
        preferred_keywords = [row['keyword'].lower() for row in cur.fetchall()]

        # 3. Get disliked article title/content keywords
        cur.execute("""
            SELECT LOWER(a.title) AS title, LOWER(COALESCE(a.content, '')) AS content
            FROM user_article_feedback f
            JOIN articles a ON a.article_id = f.article_id
            WHERE f.user_id = %s AND f.feedback_type = 'dislike'
        """, (user_id,))
        disliked_titles = []
        disliked_contents = []
        for row in cur.fetchall():
            disliked_titles.extend(row['title'].split())
            disliked_contents.extend(row['content'].split())

        # Optional: Normalize + limit
        disliked_keywords = set(disliked_titles + disliked_contents)
        disliked_keywords = {kw for kw in disliked_keywords if len(kw) > 3}  # filter stopwords

        # 4. Score each article
        for article in articles:
            score = 0
            title = article.get("title", "").lower()
            content = article.get("content", "").lower()

            # Positive scoring
            if article.get("category") in preferred_cats:
                score += 2
            if any(kw in title or kw in content for kw in preferred_keywords):
                score += 1

            # Negative scoring (strongly penalize)
            if any(kw in title or kw in content for kw in disliked_keywords):
                score -= 5  # can be filtered instead if preferred

            article["score"] = score

        cur.close()
        self.db.close()

        # Return sorted articles (optionally filter out heavily negative scores)
        return [a for a in sorted(articles, key=lambda x: x["score"], reverse=True) if a["score"] > -5]
