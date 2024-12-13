import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class OriginalUrl(BaseModel):
    url: HttpUrl


class Utm(BaseModel):
    name: str
    clicks: int


class RecordUrl(BaseModel):
    id: str
    original_url: str
    short_url: str
    created_at: datetime.datetime
    clicks: int = Field(default=0, ge=0)
    utm_tags: Optional[list[Utm]] = Field(default_factory=list)
