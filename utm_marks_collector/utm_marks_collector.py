from fastapi import Request, BackgroundTasks


async def handle_utm_marks(request: Request, id: str, url_collection, background_tasks: BackgroundTasks) -> None:
    utm_source = request.query_params.get("utm_source")
    utm_medium = request.query_params.get("utm_medium")
    utm_campaign = request.query_params.get("utm_campaign")

    if utm_source:
        background_tasks.add_task(record_utm_marks, id, url_collection, Utm(name=utm_source))
    if utm_medium:
        background_tasks.add_task(record_utm_marks, id, url_collection, Utm(name=utm_medium))
    if utm_campaign:
        background_tasks.add_task(record_utm_marks, id, url_collection, Utm(name=utm_campaign))