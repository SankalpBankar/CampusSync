import os
from pathlib import Path
ROOT = Path(__file__).resolve().parent
# Keep secrets in environment variables; the fallback key is for local development only.
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-this-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{(ROOT / 'instance' / 'campussync.db').as_posix()}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
