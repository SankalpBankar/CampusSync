from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, Committee

people_bp = Blueprint("people", __name__)

@people_bp.route("/")
@login_required
def listing():
    if current_user.role not in ("admin", "committee_head"):
        abort(403)
    if current_user.role == "admin":
        people = User.query.order_by(User.role, User.name).all()
        committees = Committee.query.order_by(Committee.name).all()
    else:
        people = User.query.filter_by(committee_id=current_user.committee_id).order_by(User.name).all()
        committees = [current_user.committee] if current_user.committee else []
    return render_template("people/list.html", people=people, committees=committees)

@people_bp.route("/create", methods=["POST"])
@login_required
def create():
    if current_user.role != "admin":
        abort(403)
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    role = request.form.get("role", "student")
    password = request.form.get("password", "")
    committee_id = request.form.get("committee_id")
    allowed_roles = {"student", "organizer", "committee_head", "admin"}
    if not name or not email or len(password) < 8 or role not in allowed_roles:
        flash("Enter valid details and a password of at least 8 characters.", "warning")
    elif User.query.filter_by(email=email).first():
        flash("That email is already registered.", "warning")
    else:
        user = User(name=name, email=email, role=role, committee_id=int(committee_id) if committee_id else None)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        if role == "committee_head" and user.committee_id:
            committee = db.session.get(Committee, user.committee_id)
            if committee:
                committee.head_id = user.id
                db.session.commit()
        flash("User created successfully.", "success")
    return redirect(url_for("people.listing"))

@people_bp.route("/<int:user_id>/role", methods=["POST"])
@login_required
def change_role(user_id):
    if current_user.role != "admin":
        abort(403)
    user = User.query.get_or_404(user_id)
    role = request.form.get("role")
    if role not in {"student", "organizer", "committee_head", "admin"}:
        abort(400)
    if user.id == current_user.id and role != "admin":
        flash("You cannot remove your own administrator role.", "warning")
    else:
        user.role = role
        db.session.commit()
        flash("Role updated.", "success")
    return redirect(url_for("people.listing"))
