import uvicorn
from django.core import management

from ..asgi import application


def initialize_db() -> None:
    management.call_command("migrate")
    management.call_command("loaddata", "carmakes")


def run() -> None:
    initialize_db()
    uvicorn.run(application, host="0.0.0.0", port=8000, log_level="info")
