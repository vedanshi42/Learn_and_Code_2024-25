from fastapi import APIRouter, HTTPException
from server.services.search_service import SearchService

router = APIRouter(prefix="/articles", tags=["Search"])
search_service = SearchService()


@router.get("")
def search_articles(category: str = None, keyword: str = None, date: str = None):
    try:
        if category:
            return search_service.search_by_category(category)
        elif keyword:
            return search_service.search_by_keyword(keyword)
        elif date:
            return search_service.search_by_date(date)
        else:
            raise HTTPException(status_code=400, detail="No search parameter provided.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching articles: {e}")
