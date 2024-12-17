import uvicorn
from django.conf import settings
from django.core import management

from ..asgi import application


def initialize_db() -> None:
    management.call_command("migrate")
    for fixture in settings.INIT_FIXTURES:
        management.call_command("loaddata", fixture)


def run() -> None:
    initialize_db()
    uvicorn.run(application, host="0.0.0.0", port=8000, log_level="info")
