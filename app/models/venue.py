from app.extensions import db
class Venue(db.Model):
    """A bookable campus location."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(180), default="")
    capacity = db.Column(db.Integer, default=0, nullable=False)
    events = db.relationship("Event", backref="venue")
