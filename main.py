from fastapi import FastAPI, Request, Path, Body
from fastapi.responses import RedirectResponse

from models.models import OriginalUrl, RecordUrl, Utm
from db.db import (
    init_db,
    create_object_in_db_mongo,
    get_object_from_db_mongo,
    get_all_objects_from_db_mongo,
    increase_the_number_of_clicks,
)

from settings.settings import DEBUG

app = FastAPI()
url_collection = init_db()


@app.post("/shorten", response_model=str)
async def create_short_url(
    url: OriginalUrl = Body(..., description="The original URL to shorten")
) -> str:
    return await create_object_in_db_mongo(url, url_collection)


@app.get("/{id}")
async def get_short_url(
    request: Request,
    id: str = Path(..., description="The ID of the short URL")
) -> RedirectResponse:
    url_data = await get_object_from_db_mongo(id, url_collection)
    query_params = request.query_params
    await increase_the_number_of_clicks(id, url_collection)
    return RedirectResponse(url=url_data.original_url)


@app.get("/stats/{id}", response_model=RecordUrl)
async def get_stats_url(
    id: str = Path(..., description="The ID of the short URL")
) -> RecordUrl:
    return await get_object_from_db_mongo(id, url_collection)


if DEBUG:

    @app.get("/urls/all", response_model=list[RecordUrl])
    async def get_all_urls() -> list[RecordUrl]:
        return await get_all_objects_from_db_mongo(url_collection)
