from fastapi import APIRouter, HTTPException
from server.services.article_service import ArticleService
from pydantic import BaseModel

router = APIRouter()
article_service = ArticleService()


class ArticleActionRequest(BaseModel):
    user_id: int
    article_id: int


@router.get("/headlines")
def get_headlines(filter_by: str = None, sort_by: str = None, user_id: int = None):
    try:
        return article_service.get_headlines(user_id=user_id, filter_by=filter_by, sort_by=sort_by)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
def save_article(req: ArticleActionRequest):
    article_service.save_article(req.user_id, req.article_id)
    return {"status": "saved"}


@router.post("/like")
def like_article(req: ArticleActionRequest):
    article_service.like_article(req.user_id, req.article_id)
    return {"status": "liked"}


@router.post("/dislike")
def dislike_article(req: ArticleActionRequest):
    article_service.dislike_article(req.user_id, req.article_id)
    return {"status": "disliked"}


@router.post("/report")
def report_article(req: ArticleActionRequest):
    article_service.report_article(req.user_id, req.article_id)
    return {"status": "reported"}
