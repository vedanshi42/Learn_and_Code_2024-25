from fastapi import APIRouter, HTTPException
from server.services.article_service import ArticleService
from server.models.article import ArticleActionRequest


router = APIRouter()
article_service = ArticleService()


@router.get("/articles/headlines")
def get_headlines(filter_by: str = None, sort_by: str = None, user_id: int = None, from_date: str = None, to_date: str = None):
    try:
        return article_service.get_headlines(user_id=user_id, filter_by=filter_by, sort_by=sort_by, from_date=from_date, to_date=to_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/articles/recommended")
def get_recommended_articles(user_id: int):
    try:
        return article_service.get_recommended_articles(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/{user_id}/saved-articles")
def save_article(user_id: int, req: ArticleActionRequest):
    try:
        article_service.save_article(user_id, req.article_id)
        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/articles/{article_id}/likes")
def like_article(article_id: int, req: ArticleActionRequest):
    try:
        article_service.like_article(req.user_id, article_id)
        return {"status": "liked"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/articles/{article_id}/dislikes")
def dislike_article(article_id: int, req: ArticleActionRequest):
    try:
        article_service.dislike_article(req.user_id, article_id)
        return {"status": "disliked"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/articles/{article_id}/reports")
def report_article(article_id: int, req: ArticleActionRequest):
    try:
        article_service.report_article(req.user_id, article_id)
        return {"status": "reported"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
