import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.getenv("DJANGO_ENV_FILEPATH", BASE_DIR / "env/dev.env"))

DEBUG: bool = bool(os.getenv("DJANGO_DEBUG"))

ALLOWED_HOSTS: list[str] = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

SECRET_KEY: str = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-dev-d6d=nm0@u_1+&f_go09c8w07-t8@z$wr*(wi(vn*$a9!bk=^o3",
)

_DB_CONFIG: dict[str, dict[str, str | Path]] = {
    "DEV": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "PROD": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("DJANGO_DB_HOST", ""),
        "PORT": os.getenv("DJANGO_DB_PORT", ""),
        "NAME": os.getenv("DJANGO_DB_NAME", ""),
        "USER": os.getenv("DJANGO_DB_USER", ""),
        "PASSWORD": os.getenv("DJANGO_DB_PASSWORD", ""),
    },
}

DATABASES: dict[str, dict[str, str | Path]] = {
    "default": _DB_CONFIG.get(
        os.getenv("DJANGO_ENVIRONMENT", "").upper(), _DB_CONFIG["DEV"]
    )
}
