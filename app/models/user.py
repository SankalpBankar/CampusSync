from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager

class User(UserMixin, db.Model):
    """User account with a role, optional committee, and optional reporting manager."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    # Roles: admin (portal administrator), committee_head, organizer, student.
    role = db.Column(db.String(30), default="student", nullable=False)
    committee_id = db.Column(db.Integer, db.ForeignKey("committee.id"))
    manager_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    manager = db.relationship("User", remote_side=[id], backref="team_members")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (ValueError, TypeError):
        return None
