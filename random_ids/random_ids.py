import time
import base64


def create_unique_id():
    timestamp = int(time.time() * 1000)
    unique_id = base64.urlsafe_b64encode(timestamp.to_bytes(8, "big")).decode("utf-8")
    return unique_id.replace("=", "").replace("+", "").replace("/", "_")
