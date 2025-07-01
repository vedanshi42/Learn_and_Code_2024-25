from server.db.db_connection import DBConnection


class PersonalizationService:
    def __init__(self):
        self.db = DBConnection()

    def score_articles(self, user_id: int, articles: list[dict]):
        cur = self.db.get_cursor()

        # Getting liked category preferences
        cur.execute("""
            SELECT c.name FROM feedback f
            JOIN articles a ON a.article_id = f.article_id
            JOIN user_categories uc ON a.category_id = uc.category_id
            JOIN categories c ON a.category_id = c.category_id
            WHERE uc.user_id = %s AND f.likes > f.dislikes
            GROUP BY c.name ORDER BY COUNT(*) DESC LIMIT 3
        """, (user_id,))
        preferred_cats = {row['name'] for row in cur.fetchall()}

        # Getting enabled or preferred keywords
        cur.execute("""
            SELECT keyword FROM keywords
            WHERE user_id = %s AND is_enabled = TRUE
        """, (user_id,))
        preferred_keywords = [row['keyword'].lower() for row in cur.fetchall()]

        # Getting disliked article title/content keywords
        cur.execute("""
            SELECT LOWER(a.title) AS title, LOWER(COALESCE(a.content, '')) AS content,
                    LOWER(a.source_url) as url
            FROM user_article_feedback f
            JOIN articles a ON a.article_id = f.article_id
            WHERE f.user_id = %s AND f.feedback_type = 'dislike'
            OR a.article_id IN (SELECT article_id from reported_articles WHERE user_id = %s)
        """, (user_id, user_id,))
        disliked_titles = []
        disliked_contents = []
        disliked_urls = []

        for row in cur.fetchall():
            disliked_titles.extend(row['title'].split())
            disliked_contents.extend(row['content'].split())
            disliked_urls.append(row['url'])

        # Normalize and get filter for words to be not included
        disliked_keywords = disliked_titles + disliked_contents
        disliked_keywords = {kw for kw in disliked_keywords if len(kw) > 3}

        # Score or give points to each article
        for article in articles:
            score = 0
            title = article.get("title", "").lower()
            content = article.get("content", "").lower()
            url = article.get('source_url', "").lower()

            # Positive scoring
            if article.get("category") in preferred_cats:
                score += 2
            if any(kw in title or kw in content for kw in preferred_keywords):
                score += 1

            # Negative scoring (strongly penalize)
            if any(kw in title or kw in content for kw in disliked_keywords):
                score -= 5

            for disliked_url in disliked_urls:
                if disliked_url.split("//")[-1].split("/")[0] in url:
                    score -= 2
                elif disliked_url in url:
                    score -= 3

            article["score"] = score

        cur.close()
        self.db.close()

        # Return sorted articles (optionally filter out heavily negative scores)
        return [article for article in articles if article["score"] > 0]
