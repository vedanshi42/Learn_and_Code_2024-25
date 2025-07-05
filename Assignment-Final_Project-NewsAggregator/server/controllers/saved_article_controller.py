from fastapi import APIRouter, HTTPException
from server.repositories.user_saved_article_repository import UserSavedArticleRepository

router = APIRouter(prefix="/users/{user_id}/saved-articles", tags=["Saved Articles"])
repo = UserSavedArticleRepository()


@router.get("")
def get_saved_articles(user_id: int):
    try:
        return repo.get_saved_articles(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching saved articles: {e}")


@router.delete("/{article_id}")
def delete_saved_article(user_id: int, article_id: int):
    try:
        repo.delete_by_id(user_id, article_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting saved article: {e}")
