import requests


class NewsAggregatorClient:
    BASE_URL = "http://localhost:8000"

    def fetch_news(self):
        try:
            response = requests.get(f"{self.BASE_URL}/fetch-news")
            response.raise_for_status()
            articles = response.json().get("articles", [])
            return articles
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
        except requests.exceptions.ConnectionError:
            print("Could not connect to the server. Is it running?")
        except requests.exceptions.Timeout:
            print("The request timed out.")
        except Exception as err:
            print(f"Unexpected error: {err}")

    def display_articles(self, articles):
        print(f"Total Articles: {len(articles)}\n")
        for i, a in enumerate(articles[:5], start=1):
            print(f"{i}. {a['title']} ({a['category']})")

    def run(self):
        print("Fetching latest news from server...")
        articles = self.fetch_news()
        self.display_articles(articles)


if __name__ == "__main__":
    app = NewsAggregatorClient()
    app.run()
