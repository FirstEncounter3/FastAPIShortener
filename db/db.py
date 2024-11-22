import datetime

from fastapi import HTTPException

from models.models import OriginalUrl, RecordUrl
from settings.settings import HOSTNAME
from random_ids.random_ids import create_unique_id


db_shorten_urls = {}


def create_object_in_db(
    url: OriginalUrl,
    utm_source: str = None,
    utm_medium: str = None,
    utm_campaign: str = None,
) -> str:
    
    id = create_unique_id()
    created_at = datetime.datetime.now()
    short_url = f"{HOSTNAME}{id}"

    db_shorten_urls[id] = RecordUrl(
        id=id, 
        original_url=url.url, 
        short_url=short_url, 
        created_at=created_at,
        utm_source=utm_source,
        utm_medium=utm_medium,
        utm_campaign=utm_campaign
    )

    return short_url


def get_object_from_db(id: str) -> RecordUrl:
    if id in db_shorten_urls:
        return db_shorten_urls[id]

    raise HTTPException(status_code=404, detail="URL not found")


#dev
def get_all_objects_from_db() -> list[RecordUrl]:
    return list(db_shorten_urls.values())
