from fastapi import APIRouter, HTTPException
from server.repositories.external_api_repository import ExternalAPIRepository
from server.repositories.category_repository import CategoryRepository
from server.repositories.keyword_repository import KeywordRepository
from server.repositories.article_repository import ArticleRepository
from server.models.admin_models import UpdateKeyRequest, CategoryRequest, DeleteArticleRequest

router = APIRouter(prefix="/admin", tags=["Admin"])

external_repo = ExternalAPIRepository()
category_repo = CategoryRepository()
keyword_repo = KeywordRepository()
article_repo = ArticleRepository()


@router.get("/external-keys")
def get_external_keys():
    try:
        return external_repo.get_all_keys()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api-keys")
def add_or_update_api_key(req: UpdateKeyRequest):
    try:
        external_repo.update_api_key(req.api_name, req.api_key)
        return {"status": "API Key updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/categories")
def get_all_categories():
    try:
        return category_repo.get_all_categories_with_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/categories")
def add_category(req: CategoryRequest):
    try:
        category_repo.add_category(req.name)
        return {"status": "Category added"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/categories/{category_name}")
def disable_category(category_name: str):
    try:
        category_repo.disable_category(category_name)
        return {"status": f"Category '{category_name}' disabled"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/keywords")
def get_all_keywords():
    try:
        return keyword_repo.get_all_keywords_with_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/keywords/{keyword}")
def disable_keyword(keyword: str):
    try:
        keyword_repo.disable_keyword_globally(keyword)
        return {"status": f"Keyword '{keyword}' disabled"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/reported-articles")
def get_reported_articles():
    try:
        return article_repo.get_reported_articles_with_counts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/articles/{article_id}")
def delete_article(article_id: int, req: DeleteArticleRequest):
    try:
        article_repo.delete_article(req.user_id, article_id)
        return {"message": "Article deleted."}
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/external-statuses")
def get_external_statuses():
    try:
        return external_repo.get_all_statuses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
