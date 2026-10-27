import os
import tempfile
import unittest
from app import create_app

class CampusSyncSmokeTests(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.app = create_app({"SQLALCHEMY_DATABASE_URI": "sqlite:///" + self.temp_db.name.replace("\\", "/")})
        self.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        self.client = self.app.test_client()

    def tearDown(self):
        try:
            os.unlink(self.temp_db.name)
        except OSError:
            pass

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CampusSync", response.data)

    def test_demo_student_can_log_in(self):
        response = self.client.post("/login", data={
            "email": "student@campussync.local", "password": "Student123!"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome back", response.data)

if __name__ == "__main__":
    unittest.main()
