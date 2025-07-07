from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from server.services.news_fetching_service import NewsFetcher
from server.services.article_service import ArticleService
from server.services.notifications_service.notification_updater import (
    NotificationsUpdater,
)


router = APIRouter(tags=["Fetch News"])
article_service = ArticleService()


@router.get("/fetch-news")
def fetch_news():
    try:
        fetcher = NewsFetcher()
        articles = fetcher.fetch_all()
        print("Updating Database")

        article_service.insert_articles(articles)
        print("Database Refreshed")

        NotificationsUpdater().update_notifications_for_all_users()

        return JSONResponse(content={"articles": [article.title for article in articles]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetch error: {str(e)}")
