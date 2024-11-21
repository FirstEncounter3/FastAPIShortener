import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl


class OriginalUrl(BaseModel):
    url: HttpUrl


class RecordUrl(BaseModel):
    id: str
    original_url: HttpUrl
    short_url: HttpUrl
    created_at: datetime.datetime
    clicks: int = 0
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None 
