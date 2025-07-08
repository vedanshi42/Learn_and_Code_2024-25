from fastapi import APIRouter, HTTPException
from server.services.saved_article_service import SavedArticleService

router = APIRouter(prefix="/users/{user_id}/saved-articles", tags=["Saved Articles"])
saved_article_service = SavedArticleService()


@router.get("")
def get_saved_articles(user_id: int):
    try:
        return saved_article_service.get_saved_articles(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching saved articles: {e}"
        )


@router.delete("/{article_id}")
def delete_saved_article(user_id: int, article_id: int):
    try:
        saved_article_service.delete_saved_article(user_id, article_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting saved article: {e}"
        )
