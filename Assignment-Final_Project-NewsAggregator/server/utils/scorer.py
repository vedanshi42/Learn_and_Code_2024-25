class ArticleScorer:
    def __init__(self, preferred_categories: set[str], keywords: set[str],
                 disliked_keywords: set[str], disliked_categories: set[str] = None):
        self.preferred_categories = preferred_categories or set()
        self.keywords = keywords or set()
        self.disliked_keywords = disliked_keywords or set()
        self.disliked_categories = disliked_categories or set()

    def score(self, article: dict):
        score = 0
        title = article['title'].lower()
        content = article['content'].lower() if article.get('content') else ""
        category = article.get('category', '').lower()

        if category in self.preferred_categories:
            score += 2
        if category in self.disliked_categories:
            score -= 2

        if any(kw in title or kw in content for kw in self.keywords):
            score += 1

        if any(kw in title or kw in content for kw in self.disliked_keywords):
            score -= 3

        return score
