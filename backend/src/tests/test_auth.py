import unittest
import json
from src.app import app  # Absolute import
from src.database.models import db, db_drop_all, setup_db, Court, CourtRegistration

# ... your test class remains the same

class CourtTestCase(unittest.TestCase):
    """This class represents the court test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.headers = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldJZm9fSE1iYTFMdDJIa3ozWkJyQyJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMjNtbjB0bjQ3aHo4ODdlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwOTQ3ODY1NzY3NjkwNDIyNzEwMyIsImF1ZCI6Imh0dHBzOi8vdWRhY2l0eS1jb2ZmZWUtYXV0aDAtYXBpLyIsImlhdCI6MTczMjM0NjIxNiwiZXhwIjoxNzMyNDMyNjE1LCJzY29wZSI6IiIsImF6cCI6ImdOU2lGb2piTTIxZFpoTDJVcWtZbnJHQmY0U0h3ZFk3IiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNvdXJ0LXJlZ2lzdHJhdGlvbnMiLCJkZWxldGU6Y291cnRzIiwiZ2V0OmNvdXJ0LXJlZ2lzdHJhdGlvbnMiLCJnZXQ6Y291cnRzIiwicGF0Y2g6Y291cnQtcmVnaXN0cmF0aW9ucyIsInBhdGNoOmNvdXJ0cyIsInBvc3Q6Y291cnQiLCJwb3N0OmNvdXJ0LXJlZ2lzdHJhdGlvbiJdfQ.chJCteBvDR4q6yfvm1ZQth6-Gr6Hj5WvZvPdD7twWx5xCd379r7nRSLJR2SRve7UNAmdaEYA1LkMAaxZ-pjcZOxoH-7fnYfKwsIKcyVzX557TUjmsk-yVeYFNkABt59i_NJ6aDkIOD3AdgCVaRWwCECJpVhdTwy98rqK2fq-WYsbCuEiFMVrTYRQfw-1r8XOT4lP20TrT_tiw_5SZiaQOl8Tx39bCgUsn2Yasf_aGpJo7uybpRbnB6Te2yABnW0FWsvKL6chZmXXg3d5e37H6tc6y_4nA9xJw6bXV7FwLHQ057bHYWAhmCZh6Ea7s-Dh6KItRGuKX3bsP6yNM0XBXA'  # Replace with a valid JWT for testing
        }
        self.test_court = {
            "name": "Test Court",
            "court_no": 1,
            "date": "2024-12-01",
            "time": "10:00",
            "max_players": 10,
            "level": "Intermediate"
        }

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_court(self):
        """Test creating a new court"""
        res = self.client().post('/courts', json=self.test_court, headers=self.headers)
        print("Input data: ", self.test_court)
        data = json.loads(res.data)
        print("Response data: ", data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('court', data)

    def test_create_court_F(self):
        """Test creating a new court"""
        res = self.client().post('/courts', json=self.test_court, headers=self.headers)
        print("Input data: ", self.test_court)
        data = json.loads(res.data)
        print("Response data: ", data)

        self.assertEqual(res.status_code, 500)
        self.assertTrue(data['success'])
        self.assertIn('court', data)

    def test_get_courts(self):
        """Test retrieving all courts"""
        # Add a court to the database for testing
        with self.app.app_context():
            court = Court(name="Test Court", court_no=1, date="2024-12-01", time="10:00", max_players=10, level="Intermediate")
            court.insert()

        res = self.client().get('/courts', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['courts'], list)

    def test_get_courts_F(self):
        """Test retrieving all courts"""
        # Add a court to the database for testing
        with self.app.app_context():
            court = Court(name="Test Court", court_no=1, date="2024-12-01", time="10:00", max_players=10, level="Intermediate")
            court.insert()

        res = self.client().get('/wrongapi', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['courts'], list)

    def test_update_court(self):
        """Test updating an existing court"""
        with self.app.app_context():
            court = Court(name="Test Court", court_no=1, date="2024-12-01", time="10:00", max_players=10, level="Intermediate")
            court.insert()

        updated_data = {
            "name": "Updated Court",
            "court_no": 2
        }
        res = self.client().patch(f'/courts/1', json=updated_data, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['court']['name'], "Updated Court")

    def test_update_court_F(self):
        """Test updating an existing court"""
        with self.app.app_context():
            court = Court(name="Test Court", court_no=1, date="2024-12-01", time="10:00", max_players=10, level="Intermediate")
            court.insert()

        updated_data = {
            "name": "Updated Court",
            "court_no": 2
        }
        res = self.client().patch(f'/courts/2', json=updated_data, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['court']['name'], "Updated Court")

    def test_delete_court(self):
        """Test deleting a court"""
        with self.app.app_context():
            court = Court(name="Test Court", court_no=1, date="2024-12-01", time="10:00", max_players=10, level="Intermediate")
            court.insert()

        res = self.client().delete(f'/courts/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_court_F(self):
        """Test deleting a court"""
        with self.app.app_context():
            court = Court(name="Test Court", court_no=1, date="2024-12-01", time="10:00", max_players=10, level="Intermediate")
            court.insert()

        res = self.client().delete(f'/courts/100', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_court_registration(self):
        """Test registering a player to a court"""
        with self.app.app_context():
            court = Court(name="Test Court", court_no=1, date="2024-12-01", time="10:00", max_players=10, level="Intermediate")
            court.insert()

        registration_data = {
            "court_id": 1,
            "name": "Player 1",
            "player_unique_id": "player1"
        }
        res = self.client().post('/court-registrations', json=registration_data, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('court_registration', data)

    def test_create_court_registration_F(self):
        """Test registering a player to a court"""
        with self.app.app_context():
            court = Court(name="Test Court", court_no=1, date="2024-12-01", time="10:00", max_players=10, level="Intermediate")
            court.insert()

        registration_data = {
            "court_id": 1,
            "name": "Player 1",
            "player_unique_id": "player1"
        }
        res = self.client().post('/court-registrations', json=registration_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['success'])
        self.assertIn('court_registration', data)

    def test_get_court_registrations(self):
        """Test retrieving registrations for a specific court"""
        with self.app.app_context():
            court = Court(name="Test Court", court_no=1, date="2024-12-01", time="10:00", max_players=10, level="Intermediate")
            court.insert()
            registration = CourtRegistration(court_id=1, name="Player 1", player_unique_id="player1", role="player", reg_date_time="2024-12-01 10:00", fee="")
            registration.insert()

        res = self.client().get(f'/court-registrations/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['registrations'], list)

    def test_get_court_registrations_F(self):
        """Test retrieving registrations for a specific court"""
        with self.app.app_context():
            court = Court(name="Test Court", court_no=1, date="2024-12-01", time="10:00", max_players=10, level="Intermediate")
            court.insert()
            registration = CourtRegistration(court_id=1, name="Player 1", player_unique_id="player1", role="player", reg_date_time="2024-12-01 10:00", fee="")
            registration.insert()

        res = self.client().get(f'/court-registrations/2', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['registrations'], list)        

if __name__ == "__main__":
    unittest.main()
