from datetime import datetime
from app.extensions import db
class Registration(db.Model):
    """Join record connecting a student to an event."""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Prevent the same student from registering for an event twice.
    __table_args__ = (db.UniqueConstraint("student_id", "event_id", name="unique_student_event"),)
