from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from server.services.notifications_service.notification_email_service import NotificationEmailService
from server.repositories.notification_repository import NotificationRepository
from server.repositories.category_repository import CategoryRepository
from server.repositories.keyword_repository import KeywordRepository


router = APIRouter()
email_service = NotificationEmailService()
repo = NotificationRepository()
notif_repo = NotificationRepository()
cat_repo = CategoryRepository()
kw_repo = KeywordRepository()


class EmailPayload(BaseModel):
    email: str


class ToggleCategoryPayload(BaseModel):
    email: str
    category: str


class ToggleKeywordPayload(BaseModel):
    email: str
    keyword: str


@router.get("/notifications/send")
def send_all_user_notifications():
    try:
        email_service.send_notifications_to_all_users()
        return {"status": "emails sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notifications/{email}")
def get_user_notifications(email: str):
    try:
        user_notifications = repo.get_notifications_for_user(email)
        return user_notifications
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notifications/categories/{email}")
def get_user_categories(email: str):
    try:
        return cat_repo.get_user_categories(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/notifications/categories/toggle")
def toggle_user_category(payload: ToggleCategoryPayload):
    try:
        cat_repo.toggle_category(payload.email, payload.category)
        return {"status": f"Category '{payload.category}' toggled"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/notifications/categories/add")
def add_user_category(payload: ToggleCategoryPayload):
    try:
        cat_repo.subscribe_user_to_category(payload.email, payload.category)
        return {"status": f"Category '{payload.category}' added for user"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/notifications/keywords/{email}")
def get_user_keywords(email: str):
    try:
        return kw_repo.get_keywords_for_user(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/notifications/keywords/toggle")
def toggle_user_keyword(payload: ToggleKeywordPayload):
    try:
        kw_repo.toggle_keyword(payload.email, payload.keyword)
        return {"status": f"Keyword '{payload.keyword}' toggled"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/notifications/keywords/add")
def add_user_keyword(payload: ToggleKeywordPayload):
    try:
        kw_repo.add_keyword_for_user(payload.email, payload.keyword)
        return {"status": f"Keyword '{payload.keyword}' added for user"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
