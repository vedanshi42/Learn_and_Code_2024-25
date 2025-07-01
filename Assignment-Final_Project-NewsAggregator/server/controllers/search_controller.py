from fastapi import APIRouter
from server.repositories.search_article_repository import SearchArticleRepository

router = APIRouter(prefix="/search", tags=["Search"])
repo = SearchArticleRepository()


@router.get("/category")
def search_by_category(category: str):
    return repo.search_by_category(category)


@router.get("/keyword")
def search_by_keyword(keyword: str):
    return repo.search_by_keyword(keyword)


@router.get("/date")
def search_by_date(date: str):
    return repo.search_by_date(date)
