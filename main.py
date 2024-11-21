from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse

from models.models import OriginalUrl
from db.db import create_object_in_db, get_object_from_db, get_all_objects_from_db

app = FastAPI()


@app.post("/shorten")
def create_short_url(
    url: OriginalUrl,
    utm_source: str = Query(None),
    utm_medium: str = Query(None),
    utm_campaign: str = Query(None),
):
    return create_object_in_db(
        url,
        utm_source=utm_source,
        utm_medium=utm_medium,
        utm_campaign=utm_campaign,
    )


@app.get("/short/{id}")
def get_short_url(id: str):
    url_data = get_object_from_db(id)
    url_data.clicks += 1
    return RedirectResponse(url=url_data.original_url)


@app.get("/stats/{id}")
def get_stats_url(id: str):
    return get_object_from_db(id)



@app.get("/all")
def get_all_urls():
    return get_all_objects_from_db()
