from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Event, Registration, Venue, Expense, User, Committee
from datetime import date, timedelta
import calendar

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def home():
    events = Event.query.filter_by(status="approved").order_by(Event.event_date).limit(6).all()
    return render_template("index.html", events=events)

@dashboard_bp.route("/dashboard")
@login_required
def index():
    if current_user.role == "student":
        registrations = Registration.query.filter_by(student_id=current_user.id).all()
        upcoming = Event.query.filter(Event.status == "approved").order_by(Event.event_date).limit(4).all()
        return render_template("dashboard/student.html", registrations=registrations, upcoming=upcoming)
    if current_user.role == "admin":
        events = Event.query.order_by(Event.event_date).all()
        pending_events = Event.query.filter_by(status="pending").order_by(Event.event_date).all()
        people = User.query.order_by(User.role, User.name).all()
        committees = Committee.query.order_by(Committee.name).all()
    elif current_user.role == "committee_head":
        events = Event.query.filter_by(committee_id=current_user.committee_id).order_by(Event.event_date).all()
        pending_events = []
        people = User.query.filter_by(committee_id=current_user.committee_id).order_by(User.name).all()
        committees = [current_user.committee] if current_user.committee else []
    else:
        events = Event.query.filter_by(created_by=current_user.id).order_by(Event.event_date).all()
        pending_events, people, committees = [], [], []
    expense_total = sum(x.amount for x in Expense.query.all()) if current_user.role == "admin" else sum(e.total_expenses for e in events)
    return render_template("dashboard/management.html", events=events, event_count=len(events),
        venue_count=Venue.query.count(), expense_total=expense_total, pending_events=pending_events,
        people=people, committees=committees, all_event_count=Event.query.count(),
        registration_count=sum(len(e.registrations) for e in events))

@dashboard_bp.route("/calendar")
@login_required
def calendar_view():
    today = date.today()
    try:
        year = int(request.args.get("year", today.year))
        month = int(request.args.get("month", today.month))
        if month < 1 or month > 12: raise ValueError
        first_weekday, days_in_month = calendar.monthrange(year, month)
    except ValueError:
        year, month = today.year, today.month
        first_weekday, days_in_month = calendar.monthrange(year, month)
    if current_user.role == "admin":
        events = Event.query.filter_by(status="approved").all()
    elif current_user.role == "student":
        events = Event.query.filter_by(status="approved").all()
    elif current_user.role == "committee_head":
        events = Event.query.filter((Event.status == "approved") | (Event.committee_id == current_user.committee_id)).all()
    else:
        events = Event.query.filter((Event.status == "approved") | (Event.created_by == current_user.id)).all()
    event_map = {}
    for event in events:
        if event.event_date.year == year and event.event_date.month == month:
            event_map.setdefault(event.event_date.day, []).append(event)
    cells = [None] * first_weekday + list(range(1, days_in_month + 1))
    while len(cells) % 7: cells.append(None)
    weeks = [cells[i:i + 7] for i in range(0, len(cells), 7)]
    previous = date(year, month, 1) - timedelta(days=1)
    next_month = date(year + (month == 12), 1 if month == 12 else month + 1, 1)
    return render_template("dashboard/calendar.html", weeks=weeks, event_map=event_map, year=year, month=month,
        month_name=calendar.month_name[month], previous=previous, next_month=next_month, today=today)

@dashboard_bp.route("/profile")
@login_required
def profile():
    return render_template("dashboard/profile.html")
