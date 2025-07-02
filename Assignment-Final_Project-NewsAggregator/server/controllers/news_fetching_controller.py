from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from server.services.news_fetching_service import NewsFetcher
from server.repositories.article_repository import ArticleRepository
from server.services.notifications_service.notification_updater import NotificationsUpdater


router = APIRouter(tags=["Fetch News"])


@router.get("/fetch-news")
def fetch_news():
    try:
        fetcher = NewsFetcher()
        articles = fetcher.fetch_all()
        print('Updating Database')

        ArticleRepository().insert_new_articles(articles)
        print("Database Refreshed")

        NotificationsUpdater().update_notifications_for_all_users()

        return JSONResponse(content={"articles": [a.title for a in articles]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetch error: {str(e)}")
