import uvicorn

from ..asgi import application


def run() -> None:
    uvicorn.run(application, host="0.0.0.0", port=8000, log_level="info")
