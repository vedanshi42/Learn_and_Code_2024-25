class ArticleScorer:
    def __init__(self, preferred_categories: set[str], keywords: list[str],
                 disliked_keywords: set[str], disliked_urls: list[str]):
        self.preferred_categories = preferred_categories
        self.keywords = keywords
        self.disliked_keywords = disliked_keywords
        self.disliked_urls = disliked_urls

    def score(self, article: dict) -> int:
        score = 0
        title = article['title'].lower()
        content = article['content'].lower() if article['content'] else ""
        url = article['source_url']
        category = article['category']

        # Positive Scoring
        if category in self.preferred_categories:
            score += 2

        if any(kw in title or kw in content for kw in self.keywords):
            score += 1

        # Negative Scoring
        if any(kw in title or kw in content for kw in self.disliked_keywords):
            score -= 5

        for disliked_url in self.disliked_urls:
            domain = disliked_url.split("//")[-1].split("/")[0]
            if domain in url:
                score -= 2
            elif disliked_url in url:
                score -= 3

        return score
