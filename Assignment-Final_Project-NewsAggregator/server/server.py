from fastapi import FastAPI
from server.controllers.article_controller import router as article_router
from server.controllers.auth_controller import router as auth_router
from server.controllers.notification_controller import router as notification_router
from server.controllers.news_fetching_controller import router as fetch_router
from server.controllers.admin_controller import router as admin_router
from server.controllers.saved_article_controller import router as saved_router
from server.controllers.search_controller import router as search_router


app = FastAPI()

app.include_router(admin_router)
app.include_router(article_router)
app.include_router(auth_router)
app.include_router(notification_router)
app.include_router(fetch_router)
app.include_router(saved_router)
app.include_router(search_router)
app.include_router(notification_router)
