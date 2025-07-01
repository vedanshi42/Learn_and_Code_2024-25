from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from server.repositories.external_api_repository import ExternalAPIRepository
from server.repositories.category_repository import CategoryRepository
from server.repositories.keyword_repository import KeywordRepository
from server.repositories.article_repository import ArticleRepository

router = APIRouter(prefix="/admin", tags=["Admin"])

external_repo = ExternalAPIRepository()
category_repo = CategoryRepository()
keyword_repo = KeywordRepository()
article_repo = ArticleRepository()


class UpdateKeyRequest(BaseModel):
    api_name: str
    api_key: str


class CategoryRequest(BaseModel):
    name: str


class KeywordRequest(BaseModel):
    word: str


class DeleteArticleRequest(BaseModel):
    user_id: int


@router.get("/external-statuses")
def get_external_statuses():
    return external_repo.get_all_statuses()


@router.get("/external-keys")
def get_external_keys():
    return external_repo.get_all_keys()


@router.post("/update-key")
def update_key(req: UpdateKeyRequest):
    external_repo.update_api_key(req.api_name, req.api_key)
    return {"status": "API Key updated"}


@router.post("/add-category")
def add_category(req: CategoryRequest):
    category_repo.add_category(req.name)
    return {"status": "Category added"}


@router.post("/disable-category")
def disable_category(req: CategoryRequest):
    try:
        category_repo.disable_category(req.name)
        return {"status": f"Category '{req.name}' disabled"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/categories")
def get_all_categories():
    try:
        return category_repo.get_all_categories_with_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/disable-keyword")
def disable_keyword(req: KeywordRequest):
    try:
        keyword_repo.disable_keyword_globally(req.word)
        return {"status": f"Keyword '{req.word}' disabled"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/keywords")
def get_all_keywords():
    try:
        return keyword_repo.get_all_keywords_with_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reported-articles")
def get_reported_articles():
    try:
        return article_repo.get_reported_articles_with_counts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-article/{article_id}")
def delete_article(article_id: int, req: DeleteArticleRequest):
    try:
        article_repo.delete_article(req.user_id, article_id)
        return {"message": "Article deleted."}
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting article: {e}")
