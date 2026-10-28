from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Venue, Event
venues_bp = Blueprint("venues", __name__)

# Only admins can create or remove venues; signed-in users can view them.
@venues_bp.route("/")
@login_required
def listing():
    return render_template("venues/list.html", venues=Venue.query.order_by(Venue.name).all())

@venues_bp.route("/create", methods=["POST"])
@login_required
def create():
    if current_user.role != "admin": abort(403)
    name = request.form.get("name", "").strip()
    try:
        capacity = int(request.form.get("capacity", "0"))
        if not name or capacity < 1: raise ValueError
        if Venue.query.filter_by(name=name).first():
            flash("Venue already exists.", "warning")
        else:
            db.session.add(Venue(name=name, location=request.form.get("location", "").strip(), capacity=capacity))
            db.session.commit(); flash("Venue added.", "success")
    except ValueError:
        flash("Enter a name and positive capacity.", "warning")
    return redirect(url_for("venues.listing"))

@venues_bp.route("/<int:venue_id>/delete", methods=["POST"])
@login_required
def delete(venue_id):
    if current_user.role != "admin": abort(403)
    venue = Venue.query.get_or_404(venue_id)
    if Event.query.filter_by(venue_id=venue.id).first():
        flash("Venue is assigned to an event and cannot be deleted.", "warning")
    else:
        db.session.delete(venue); db.session.commit(); flash("Venue deleted.", "info")
    return redirect(url_for("venues.listing"))
