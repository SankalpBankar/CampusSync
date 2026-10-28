from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Event, Expense
finance_bp = Blueprint("finance", __name__)

def can_manage(event):
    # Coordinators can manage finances only for events they created.
    return current_user.role == "admin" or (current_user.role == "committee_head" and event.committee_id == current_user.committee_id) or (current_user.role == "organizer" and event.created_by == current_user.id)

@finance_bp.route("/")
@login_required
def overview():
    if current_user.role == "student": abort(403)
    events = Event.query.order_by(Event.event_date.desc()).all()
    if current_user.role == "organizer":
        events = [event for event in events if event.created_by == current_user.id]
    elif current_user.role == "committee_head":
        events = [event for event in events if event.committee_id == current_user.committee_id]
    return render_template("finance/overview.html", events=events)

@finance_bp.route("/<int:event_id>/expenses", methods=["GET", "POST"])
@login_required
def expenses(event_id):
    event = Event.query.get_or_404(event_id)
    if not can_manage(event): abort(403)
    if request.method == "POST":
        description = request.form.get("description", "").strip()
        try:
            amount = float(request.form.get("amount", "0"))
            if not description or amount <= 0: raise ValueError
            if event.total_expenses + amount > event.budget:
                flash("Expense exceeds the remaining budget.", "warning")
            else:
                db.session.add(Expense(event_id=event.id, description=description, amount=amount, created_by=current_user.id))
                db.session.commit(); flash("Expense recorded.", "success")
                return redirect(url_for("finance.expenses", event_id=event.id))
        except ValueError:
            flash("Enter a description and positive amount.", "warning")
    return render_template("finance/expenses.html", event=event)
