from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Event, Registration, Venue
events_bp = Blueprint("events", __name__)

def allowed(event=None):
    if current_user.role == "admin":
        return True
    if current_user.role == "committee_head":
        return event is None or event.committee_id == current_user.committee_id
    if current_user.role == "organizer":
        return event is None or event.created_by == current_user.id
    return False

def conflict(venue_id, date, start, end, skip=None):
    # Two bookings conflict when they share a venue/date and their time ranges overlap.
    q = Event.query.filter(Event.venue_id == venue_id, Event.event_date == date,
        Event.start_time < end, Event.end_time > start)
    if skip:
        # When editing, don't treat the event's existing booking as a conflict.
        q = q.filter(Event.id != skip)
    return q.first() is not None

@events_bp.route("/")
def listing():
    query = Event.query.filter_by(status="approved")
    if current_user.is_authenticated and current_user.role == "admin":
        query = Event.query
    elif current_user.is_authenticated and current_user.role in ("committee_head", "organizer"):
        query = Event.query.filter((Event.status == "approved") | (Event.created_by == current_user.id))
    return render_template("events/list.html", events=query.order_by(Event.event_date).all())

@events_bp.route("/<int:event_id>")
def detail(event_id):
    event = Event.query.get_or_404(event_id)
    registered = current_user.is_authenticated and Registration.query.filter_by(student_id=current_user.id, event_id=event.id).first()
    return render_template("events/detail.html", event=event, registered=bool(registered))

@events_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if current_user.role not in ("admin", "committee_head", "organizer"): abort(403)
    venues = Venue.query.order_by(Venue.name).all()
    if request.method == "POST":
        try:
            date = datetime.strptime(request.form["event_date"], "%Y-%m-%d").date()
            start = datetime.strptime(request.form["start_time"], "%H:%M").time()
            end = datetime.strptime(request.form["end_time"], "%H:%M").time()
            budget = float(request.form.get("budget", 0))
            venue_id = int(request.form["venue_id"]) if request.form.get("venue_id") else None
            title = request.form.get("title", "").strip()
            if not title or end <= start or budget < 0: raise ValueError
            # Check venue conflicts before saving a new event.
            if venue_id and conflict(venue_id, date, start, end):
                flash("Venue is already booked during that time.", "danger")
            else:
                event = Event(title=title, description=request.form.get("description", "").strip(),
                    category=request.form.get("category", "General"), event_date=date, start_time=start,
                    end_time=end, budget=budget, venue_id=venue_id, created_by=current_user.id,
                    committee_id=(current_user.committee_id if current_user.role != "admin" else (int(request.form.get("committee_id")) if request.form.get("committee_id") else None)),
                    status="approved" if current_user.role == "admin" else "pending")
                db.session.add(event); db.session.commit()
                flash("Event created." if event.status == "approved" else "Event proposal submitted for administrator approval.", "success")
                return redirect(url_for("events.detail", event_id=event.id))
        except (ValueError, KeyError, TypeError):
            flash("Check the event details and time range.", "warning")
    return render_template("events/form.html", event=None, venues=venues)

@events_bp.route("/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def edit(event_id):
    event = Event.query.get_or_404(event_id)
    if not allowed(event): abort(403)
    venues = Venue.query.order_by(Venue.name).all()
    if request.method == "POST":
        try:
            date = datetime.strptime(request.form["event_date"], "%Y-%m-%d").date()
            start = datetime.strptime(request.form["start_time"], "%H:%M").time()
            end = datetime.strptime(request.form["end_time"], "%H:%M").time()
            budget = float(request.form.get("budget", 0))
            venue_id = int(request.form["venue_id"]) if request.form.get("venue_id") else None
            title = request.form.get("title", "").strip()
            if not title or end <= start or budget < 0: raise ValueError
            if venue_id and conflict(venue_id, date, start, end, event.id):
                flash("Venue is already booked during that time.", "danger")
            else:
                event.title, event.description = title, request.form.get("description", "").strip()
                event.category, event.event_date = request.form.get("category", "General"), date
                event.start_time, event.end_time, event.budget, event.venue_id = start, end, budget, venue_id
                db.session.commit()
                flash("Event updated.", "success")
                return redirect(url_for("events.detail", event_id=event.id))
        except (ValueError, KeyError, TypeError):
            flash("Check the event details and time range.", "warning")
    return render_template("events/form.html", event=event, venues=venues)

@events_bp.route("/<int:event_id>/delete", methods=["POST"])
@login_required
def delete(event_id):
    event = Event.query.get_or_404(event_id)
    if not allowed(event): abort(403)
    db.session.delete(event); db.session.commit()
    flash("Event deleted.", "info")
    return redirect(url_for("events.listing"))

@events_bp.route("/<int:event_id>/register", methods=["POST"])
@login_required
def register(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user.role != "student":
        abort(403)
    if Registration.query.filter_by(student_id=current_user.id, event_id=event.id).first():
        flash("You are already registered.", "info")
    elif event.status != "approved":
        flash("This event is not open for registration yet.", "warning")
    elif event.event_date < datetime.today().date():
        flash("Registration is closed for past events.", "warning")
    else:
        db.session.add(Registration(student_id=current_user.id, event_id=event.id))
        db.session.commit()
        flash("Registration successful.", "success")
    return redirect(url_for("events.detail", event_id=event.id))

@events_bp.route("/<int:event_id>/review", methods=["POST"])
@login_required
def review(event_id):
    if current_user.role != "admin":
        abort(403)
    event = Event.query.get_or_404(event_id)
    decision = request.form.get("decision")
    if decision not in ("approved", "rejected"):
        abort(400)
    event.status = decision
    db.session.commit()
    flash(f"Event {decision}.", "success")
    return redirect(url_for("dashboard.index"))
