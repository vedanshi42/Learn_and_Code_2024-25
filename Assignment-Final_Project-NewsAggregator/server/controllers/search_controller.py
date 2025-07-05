from fastapi import APIRouter, HTTPException
from server.repositories.search_article_repository import SearchArticleRepository

router = APIRouter(prefix="/articles", tags=["Search"])
repo = SearchArticleRepository()


@router.get("")
def search_articles(category: str = None, keyword: str = None, date: str = None):
    try:
        if category:
            return repo.search_by_category(category)
        elif keyword:
            return repo.search_by_keyword(keyword)
        elif date:
            return repo.search_by_date(date)
        else:
            raise HTTPException(status_code=400, detail="No search parameter provided.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching articles: {e}")
