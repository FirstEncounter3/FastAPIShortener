from fastapi import FastAPI, Query, Path, Body
from fastapi.responses import RedirectResponse

from models.models import OriginalUrl, RecordUrl
# from db.db import init_db, get_object_from_db, get_all_objects_from_db
from db.db import init_db, create_object_in_db_mongo, get_object_from_db_mongo, get_all_objects_from_db_mongo

from settings.settings import DEBUG

app = FastAPI()
url_collection = init_db()

@app.post("/shorten", response_model=str)
async def create_short_url(
    url: OriginalUrl = Body(..., description="The original URL to shorten"),
    # utm_source: str = Query(None, description="The utm_source parameter"),
    # utm_medium: str = Query(None, description="The utm_medium parameter"),
    # utm_campaign: str = Query(None, description="The utm_campaign parameter"),
) -> str:
    return await create_object_in_db_mongo(
        url,
        url_collection
        # utm_source=utm_source,
        # utm_medium=utm_medium,
        # utm_campaign=utm_campaign,
    )


@app.get("/{id}")
async def get_short_url(id: str = Path(..., description="The ID of the short URL")) -> RedirectResponse:
    url_data = await get_object_from_db_mongo(id, url_collection)
    url_data.clicks += 1
    return RedirectResponse(url=url_data.original_url)


@app.get("/stats/{id}", response_model=RecordUrl)
async def get_stats_url(id: str = Path(..., description="The ID of the short URL")) -> RecordUrl:
    return await get_object_from_db_mongo(id, url_collection)


if DEBUG:
    @app.get("/urls/all", response_model=list[RecordUrl])
    async def get_all_urls() -> list[RecordUrl]:
        return await get_all_objects_from_db_mongo(url_collection)
