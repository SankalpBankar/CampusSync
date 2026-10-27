from datetime import datetime
from app.extensions import db

class Event(db.Model):
    """Campus event, including its review state and committee ownership."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, default="")
    category = db.Column(db.String(80), default="General")
    event_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"))
    budget = db.Column(db.Float, default=0, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    committee_id = db.Column(db.Integer, db.ForeignKey("committee.id"))
    status = db.Column(db.String(20), default="approved", nullable=False)  # pending / approved / rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator = db.relationship("User", foreign_keys=[created_by], backref="created_events")
    committee = db.relationship("Committee", backref="events")
    registrations = db.relationship("Registration", backref="event", cascade="all, delete-orphan")
    expenses = db.relationship("Expense", backref="event", cascade="all, delete-orphan")

    @property
    def total_expenses(self):
        return sum(item.amount for item in self.expenses)
