from functools import wraps
from server.services.personalization_service import PersonalizationService
from server.db.db_connection import DBConnection


def personalize_articles(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        articles = func(self, *args, **kwargs)
        user_id = kwargs.get("user_id")

        if not user_id:
            return articles

        service = PersonalizationService()
        return sorted(service.score_articles(user_id, articles), key=lambda x: x["score"], reverse=True)

    return wrapper


def personalize_notifications(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        notifications = func(self, *args, **kwargs)
        email = kwargs.get("email")

        if not email or not notifications:
            return notifications

        db = DBConnection()
        cur = db.get_cursor()
        cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        db.close()

        if not user:
            return notifications

        user_id = user["user_id"]
        service = PersonalizationService()
        return sorted(service.score_articles(user_id, notifications), key=lambda x: x["score"], reverse=True)

    return wrapper
