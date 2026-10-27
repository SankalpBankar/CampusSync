from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# Shared extensions are initialized by create_app() to avoid circular imports.
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
