from fastapi import APIRouter, HTTPException
from server.services.admin_service import AdminService
from server.models.admin_models import (
    UpdateKeyRequest,
    CategoryRequest,
    DeleteArticleRequest,
)

router = APIRouter(prefix="/admin", tags=["Admin"])
admin_service = AdminService()


@router.get("/external-keys")
def get_external_keys():
    try:
        return admin_service.get_external_keys()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api-keys")
def add_or_update_api_key(req: UpdateKeyRequest):
    try:
        admin_service.update_api_key(req.api_name, req.api_key)
        return {"status": "API Key updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/categories")
def get_all_categories():
    try:
        return admin_service.get_all_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/categories")
def add_category(req: CategoryRequest):
    try:
        admin_service.add_category(req.name)
        return {"status": "Category added"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/categories/{category_name}")
def disable_category(category_name: str):
    try:
        admin_service.disable_category(category_name)
        return {"status": f"Category '{category_name}' disabled"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/keywords")
def get_all_keywords():
    try:
        return admin_service.get_all_keywords()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/keywords/{keyword}")
def disable_keyword(keyword: str):
    try:
        admin_service.disable_keyword_globally(keyword)
        return {"status": f"Keyword '{keyword}' disabled"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/reported-articles")
def get_reported_articles():
    try:
        return admin_service.get_reported_articles()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/articles/{article_id}")
def delete_article(article_id: int, req: DeleteArticleRequest):
    try:
        admin_service.delete_article(req.user_id, article_id)
        return {"message": "Article deleted."}
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/external-statuses")
def get_external_statuses():
    try:
        return admin_service.get_external_statuses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
