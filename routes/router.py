from fastapi import APIRouter, BackgroundTasks, Request, Path, Body
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

from models.models import OriginalUrl, RecordUrl, Utm
from exceptions.exceptions import DatabaseError, UrlNotFound
from db.db import (
    init_db,
    create_object_in_db_mongo,
    get_object_from_db_mongo,
    get_all_objects_from_db_mongo,
    increase_the_number_of_clicks,
    record_utm_marks,
)

from utm_marks_collector.utm_marks_collector import handle_utm_marks

from settings.settings import DEBUG

router = APIRouter()
url_collection = init_db('shortener')

@router.post("/shorten", response_model=str)
async def create_short_url(
    url: OriginalUrl = Body(..., description="The original URL to shorten")
) -> str:
    try:
        return await create_object_in_db_mongo(url, url_collection)
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}")
async def get_short_url(
    request: Request,
    background_tasks: BackgroundTasks,
    id: str = Path(..., description="The ID of the short URL")
) -> RedirectResponse:
    try:
        url_data = await get_object_from_db_mongo(id, url_collection)
    except UrlNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    await increase_the_number_of_clicks(id, url_collection)
    await handle_utm_marks(request, id, url_collection, background_tasks)

    return RedirectResponse(url=url_data.original_url)


@router.get("/stats/{id}", response_model=RecordUrl)
async def get_stats_url(
    id: str = Path(..., description="The ID of the short URL")
) -> RecordUrl:
    try:
        return await get_object_from_db_mongo(id, url_collection)
    except UrlNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


if DEBUG:

    @router.get("/urls/all", response_model=list[RecordUrl])
    async def get_all_urls() -> list[RecordUrl]:
        return await get_all_objects_from_db_mongo(url_collection)
