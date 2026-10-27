# CampusSync — Campus Event Management System

**CampusSync** is a web-based Campus Event Management System designed to simplify the planning, organization, and management of college events. It provides a centralized platform where administrators and event coordinators can manage events, student registrations, venue bookings, and event budgets.

The project aims to reduce manual coordination, improve resource utilization, and make campus event management more organized and efficient.

## ✨ Features

- **User Authentication:** Secure login and logout functionality.
- **Role-Based Access:** Separate access for administrators, coordinators, and students.
- **Event Management:** Create, view, update, and manage campus events.
- **Student Registration:** Allow students to browse events and register for participation.
- **Venue Management:** Manage venue bookings and check for scheduling conflicts.
- **Budget Management:** Track event budgets and record expenses.
- **Dashboard:** Display relevant event and management information based on user roles.
- **Responsive Interface:** Access the application through a clean, user-friendly web interface.

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript, Bootstrap |
| Backend | Python, Flask |
| Database | SQLite |
| ORM | Flask-SQLAlchemy |
| Authentication | Flask-Login |
| Testing | Python unittest / pytest |

## 📁 Project Structure

```text
CampusSync/
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── event.py
│   │   ├── registration.py
│   │   ├── venue.py
│   │   └── expense.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── events.py
│   │   ├── venues.py
│   │   └── finance.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── events/
│   │   ├── venues/
│   │   └── finance/
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── main.js
│       └── images/
│
├── tests/
│   ├── test_auth.py
│   ├── test_events.py
│   └── test_venues.py
│
├── config.py
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

Follow these steps to run CampusSync locally.

### 1. Clone the repository

```bash
git clone https://github.com/SankalpBankar/CampusSync.git
cd CampusSync
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it using the appropriate command.

**Windows — Command Prompt:**

```bash
venv\Scripts\activate
```

**Windows — Git Bash:**

```bash
source venv/Scripts/activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Example:

```env
SECRET_KEY=replace_with_a_secure_random_secret
DATABASE_URL=sqlite:///campussync.db
```

Make sure `.env` is included in `.gitignore`. Do not commit production secrets or credentials to GitHub.

### 5. Initialize the database

Ensure your Flask application is configured to initialize the database tables. If your project uses `db.create_all()` during application setup, the tables can be created automatically when the application initializes.

If you use database migrations instead, follow the migration instructions implemented in your project.

### 6. Run the application

```bash
python run.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

The exact startup command and database initialization steps should match the implementation in your repository.

## 👥 User Roles

### Administrator
- Manage user accounts and permissions.
- Oversee campus events and related activities.
- Monitor venue bookings and event finances.

### Event Coordinator
- Create and manage events.
- Review registrations.
- Request or manage venue bookings.
- Track event budgets and expenses.

### Student
- Browse available campus events.
- View event details and schedules.
- Register for events.

*Available actions depend on the permissions implemented in the application.*

## 🗄️ Database Design

CampusSync uses SQLite for local data storage, with Flask-SQLAlchemy managing database interactions.

The primary models include:

- **User:** Stores user account information and roles.
- **Event:** Stores event details, schedules, and related information.
- **Registration:** Connects students with the events they register for.
- **Venue:** Stores venue information and booking details.
- **Expense:** Records expenses associated with campus events.

Relationships between these models help maintain consistency and organize event-related data.

## 🧪 Testing

Run the project's automated tests using:

```bash
python -m unittest discover -s tests
```

If the project uses pytest and it is installed, you can alternatively run:

```bash
pytest
```

Ensure the test files are implemented and configured before relying on the results.

## 🔮 Future Enhancements

The following features may be considered for future development:

- QR-code-based attendance tracking.
- Email notifications and event reminders.
- Sponsor directory and sponsorship tracking.
- Committee-specific dashboards and permissions.
- Event analytics and reporting.
- Online payment integration for paid events.
- Migration to PostgreSQL for larger deployments.
- Integration with university systems.
- Mobile-friendly enhancements and a dedicated mobile application.

## 🔐 Security Considerations

- Store passwords using secure password hashing.
- Keep secret keys and sensitive configuration out of source control.
- Enforce role-based authorization on protected routes.
- Validate user input and prevent unauthorized modifications.
- Use secure deployment settings before exposing the application publicly.

## 🎯 Project Objective

The objective of CampusSync is to provide a centralized and maintainable platform for managing campus events, student registrations, venue scheduling, and event finances while reducing manual administrative work.

## 👨‍💻 Contributors

Developed as an academic project by **Sankalp Bankar**.
