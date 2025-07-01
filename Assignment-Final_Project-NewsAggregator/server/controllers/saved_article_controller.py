from fastapi import APIRouter
from server.repositories.user_saved_article_repository import UserSavedArticleRepository

router = APIRouter(prefix="/saved", tags=["Saved Articles"])
repo = UserSavedArticleRepository()


@router.get("/{user_id}")
def get_saved_articles(user_id: int):
    return repo.get_saved_articles(user_id)


@router.delete("/{user_id}/{article_id}")
def delete_saved_article(user_id: int, article_id: int):
    repo.delete_by_id(user_id, article_id)
    return {"status": "deleted"}
