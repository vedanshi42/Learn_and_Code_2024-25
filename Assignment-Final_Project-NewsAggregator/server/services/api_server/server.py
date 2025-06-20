from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from server.services.news_fetching_service import NewsFetcher
from server.exceptions.api_exception import ApiException

app = FastAPI()


@app.get("/fetch-news")
def fetch_news():
    try:
        fetcher = NewsFetcher()
        articles = fetcher.fetch_all()

        serialized = [
            {
                "title": a.title,
                "content": a.content,
                "url": a.source_url,
                "published": a.date_published.isoformat(),
                "category": a.category
            } for a in articles
        ]
        return JSONResponse(content={"articles": serialized})
    
    except ApiException as ae:
        raise HTTPException(status_code=ae.status_code, detail=str(ae))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
