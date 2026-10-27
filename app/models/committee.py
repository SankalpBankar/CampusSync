from app.extensions import db

class Committee(db.Model):
    """A campus club or committee that owns events and has a head."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(300), default="")
    head_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    members = db.relationship("User", backref="committee", foreign_keys="User.committee_id")
    head = db.relationship("User", foreign_keys=[head_id], post_update=True)
