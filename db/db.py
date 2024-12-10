import datetime

from fastapi import HTTPException
from pydantic import ValidationError
from motor.motor_asyncio import AsyncIOMotorClient

from models.models import OriginalUrl, RecordUrl
from settings.settings import HOSTNAME, MONGO_HOST
from random_ids.random_ids import create_unique_id


def init_db(db_name):
    client = AsyncIOMotorClient(MONGO_HOST)
    database = client[db_name]
    url_collection = database.get_collection("urls")

    return url_collection


async def create_object_in_db_mongo(url: OriginalUrl, url_collection) -> str:
    id = create_unique_id()
    created_at = datetime.datetime.now()
    short_url = f"{HOSTNAME}{id}"
    original_url = str(url.url)
    
    try:
        record = RecordUrl(
            id=id,
            original_url=original_url,
            short_url=short_url,
            created_at=created_at,
            clicks=0,
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    await url_collection.insert_one(record.model_dump())

    return short_url


async def get_object_from_db_mongo(id: str, url_collection) -> RecordUrl:
    url_data = await url_collection.find_one({"id": id})

    if url_data:
        return RecordUrl(**url_data)

    raise HTTPException(status_code=404, detail="URL not found")


async def increase_the_number_of_clicks(id: str, url_collection) -> RecordUrl:
    url_data = await url_collection.find_one({"id": id})

    if url_data:
        try:
            clicks = url_data["clicks"] + 1
            await url_collection.update_one({"id": id}, {"$set": {"clicks": clicks}})

            return RecordUrl(**url_data)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

    raise HTTPException(status_code=404, detail="URL not found")


async def get_all_objects_from_db_mongo(url_collection) -> list[RecordUrl]:
    urls = [RecordUrl(**url_data) async for url_data in url_collection.find()]
    return urls
