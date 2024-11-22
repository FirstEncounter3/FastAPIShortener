from fastapi import FastAPI, Query, Path, Body
from fastapi.responses import RedirectResponse

from models.models import OriginalUrl, RecordUrl
from db.db import create_object_in_db, get_object_from_db, get_all_objects_from_db

from settings.settings import DEBUG

app = FastAPI()


@app.post("/shorten", response_model=str)
def create_short_url(
    url: OriginalUrl = Body(..., description="The original URL to shorten"),
    utm_source: str = Query(None, description="The utm_source parameter"),
    utm_medium: str = Query(None, description="The utm_medium parameter"),
    utm_campaign: str = Query(None, description="The utm_campaign parameter"),
) -> str:
    return create_object_in_db(
        url,
        utm_source=utm_source,
        utm_medium=utm_medium,
        utm_campaign=utm_campaign,
    )


@app.get("/{id}")
def get_short_url(id: str = Path(..., description="The ID of the short URL")) -> RedirectResponse:
    url_data = get_object_from_db(id)
    url_data.clicks += 1
    return RedirectResponse(url=url_data.original_url)


@app.get("/stats/{id}", response_model=RecordUrl)
def get_stats_url(id: str = Path(..., description="The ID of the short URL")) -> RecordUrl:
    return get_object_from_db(id)


if DEBUG:
    @app.get("/urls/all", response_model=list[RecordUrl])
    def get_all_urls() -> list[RecordUrl]:
        return get_all_objects_from_db()
