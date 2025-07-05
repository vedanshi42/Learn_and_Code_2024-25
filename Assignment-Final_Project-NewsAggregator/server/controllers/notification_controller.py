from fastapi import APIRouter, HTTPException
from server.services.notifications_service.notification_email_service import NotificationEmailService
from server.services.notifications_service.notification_configurator import NotificationsConfigurator
from server.models.notification_models import ToggleCategoryPayload, ToggleKeywordPayload


router = APIRouter()
email_service = NotificationEmailService()
notification_config = NotificationsConfigurator()


@router.post("/users/notifications/send")
def send_all_user_notifications():
    try:
        email_service.send_notifications_to_all_users()
        return {"status": "emails sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get, add, and toggle categories for a user
@router.get("/users/{user_id}/categories")
def get_user_categories(user_id: int):
    try:
        return notification_config.get_user_categories(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/{user_id}/categories")
def add_user_category(user_id: int, payload: ToggleCategoryPayload):
    try:
        notification_config.add_category_for_user(user_id, payload.category)
        return {"status": f"Category '{payload.category}' added for user"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/users/{user_id}/categories/{category}")
def toggle_user_category(user_id: int, category: str):
    try:
        notification_config.toggle_category(user_id, category)
        return {"status": f"Category '{category}' toggled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get, add, and toggle keywords for a user
@router.get("/users/{user_id}/keywords")
def get_user_keywords(user_id: int):
    try:
        return notification_config.get_user_keywords(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/{user_id}/keywords")
def add_user_keyword(user_id: int, payload: ToggleKeywordPayload):
    try:
        notification_config.add_keyword_for_user(user_id, payload.keyword)
        return {"status": f"Keyword '{payload.keyword}' added for user"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/users/{user_id}/keywords/{keyword}")
def toggle_user_keyword(user_id: int, keyword: str):
    try:
        notification_config.toggle_keyword(user_id, keyword)
        return {"status": f"Keyword '{keyword}' toggled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get notifications for a user
@router.get("/users/{user_id}/notifications")
def get_user_notifications(user_id: int):
    try:
        return notification_config.get_user_notifications(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
