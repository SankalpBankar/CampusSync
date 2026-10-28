import os
from datetime import date, time, timedelta
from flask import Flask
from config import Config
from app.extensions import db, login_manager
from sqlalchemy import inspect, text

def create_app(test_config=None):
    """Create the Flask app and seed illustrative local demo records."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    from app.models import User, Committee, Event, Registration, Venue, Expense
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.events import events_bp
    from app.routes.venues import venues_bp
    from app.routes.finance import finance_bp
    from app.routes.people import people_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(events_bp, url_prefix="/events")
    app.register_blueprint(venues_bp, url_prefix="/venues")
    app.register_blueprint(finance_bp, url_prefix="/finance")
    app.register_blueprint(people_bp, url_prefix="/people")
    with app.app_context():
        db.create_all()
        migrate_legacy_sqlite_schema(app)
        seed_demo_data()
    return app

def seed_demo_data():
    """Seed demo accounts, committees, venues, and sample events once only."""
    from app.models import User, Committee, Event, Venue
    accounts = [
        ("Campus Administrator", "admin@campussync.local", "Admin123!", "admin"),
        ("Priya Sharma", "head@campussync.local", "Head123!", "committee_head"),
        ("Rahul Verma", "organizer@campussync.local", "Organizer123!", "organizer"),
        ("Sankalp Bankar", "student@campussync.local", "Student123!", "student"),
    ]
    users = {}
    for name, email, password, role in accounts:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(name=name, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
        users[role] = user
    committee = Committee.query.filter_by(name="Technical Council").first()
    if not committee:
        committee = Committee(name="Technical Council", description="Technical festivals, coding events and workshops", head_id=users["committee_head"].id)
        db.session.add(committee)
        db.session.flush()
    users["committee_head"].committee_id = committee.id
    users["organizer"].committee_id = committee.id
    users["organizer"].manager_id = users["committee_head"].id
    venues_data = [("Main Auditorium", "Academic Block", 800), ("Innovation Lab", "CSE Building", 120), ("Seminar Hall 2", "Academic Block", 180), ("Open Air Theatre", "Central Campus", 600)]
    venues = {}
    for name, location, capacity in venues_data:
        venue = Venue.query.filter_by(name=name).first()
        if not venue:
            venue = Venue(name=name, location=location, capacity=capacity)
            db.session.add(venue)
            db.session.flush()
        venues[name] = venue
    db.session.commit()
    # Use relative future dates so the demo homepage is never stuck with past events.
    if Event.query.count() == 0:
        today = date.today()
        samples = [
            ("TechTalk: Polaris", "A practical session on emerging technologies, developer tools and career pathways.", "Technical", 7, time(10, 0), time(12, 0), "Main Auditorium", 25000, "approved", "organizer"),
            ("Photography Workshop: Pratishruti", "Learn composition, lighting and visual storytelling in this beginner-friendly workshop.", "Workshop", 12, time(14, 0), time(16, 0), "Seminar Hall 2", 8000, "approved", "organizer"),
            ("Battle of Bands: Akarshan", "A campus music showcase featuring student performers and live bands.", "Cultural", 18, time(17, 0), time(20, 0), "Open Air Theatre", 40000, "approved", "committee_head"),
            ("BuildSprint: Student Hackathon", "A team-based build sprint for prototypes addressing real campus and community problems.", "Hackathon", 23, time(9, 0), time(17, 0), "Innovation Lab", 30000, "approved", "organizer"),
            ("AI and Data Science Meetup", "Student talks and demos covering machine learning, generative AI and responsible AI.", "Seminar", 29, time(11, 0), time(13, 0), "Seminar Hall 2", 12000, "pending", "organizer"),
            ("Design for Good Ideathon", "Collaborative ideation session for accessible and sustainable digital solutions.", "Competition", 35, time(10, 0), time(15, 0), "Innovation Lab", 15000, "approved", "committee_head"),
        ]
        for title, desc, category, days, start, end, venue_name, budget, status, creator_role in samples:
            db.session.add(Event(title=title, description=desc, category=category, event_date=today + timedelta(days=days), start_time=start, end_time=end, venue_id=venues[venue_name].id, budget=budget, created_by=users[creator_role].id, committee_id=committee.id, status=status))
        db.session.commit()

def migrate_legacy_sqlite_schema(app):
    """Add columns introduced in this version when an older local SQLite DB exists."""
    if not app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        return
    inspector = inspect(db.engine)
    additions = {
        "user": {"committee_id": "INTEGER", "manager_id": "INTEGER"},
        "event": {"committee_id": "INTEGER", "status": "VARCHAR(20) NOT NULL DEFAULT 'approved'"},
    }
    with db.engine.begin() as connection:
        for table, columns in additions.items():
            if table not in inspector.get_table_names():
                continue
            existing = {column["name"] for column in inspector.get_columns(table)}
            for column, sql_type in columns.items():
                if column not in existing:
                    connection.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {sql_type}"))
