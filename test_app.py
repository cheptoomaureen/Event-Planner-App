import unittest
import json
from app import app, db
from models import User, Event, Task, Resource, Expense, Notification
from werkzeug.security import generate_password_hash

class EventPlannerAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        response = self.app.post('/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('User registered successfully', response.json['message'])

    def test_login_user(self):
        # Register user first
        self.app.post('/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        # Attempt login
        response = self.app.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_create_event(self):
        # Register and login user first
        self.app.post('/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        login_response = self.app.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        token = login_response.json['token']
        
        response = self.app.post('/events', json={
            'title': 'Test Event',
            'date': '2024-01-01T00:00:00',
            'location': 'Test Location',
            'description': 'Test Description'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Event created successfully', response.json['message'])

    def test_create_task(self):
        # Register and login user first
        self.app.post('/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        login_response = self.app.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        token = login_response.json['token']
        
        # Create an event first
        self.app.post('/events', json={
            'title': 'Test Event',
            'date': '2024-01-01T00:00:00',
            'location': 'Test Location',
            'description': 'Test Description'
        }, headers={'Authorization': f'Bearer {token}'})
        
        event_id = Event.query.first().id

        response = self.app.post('/tasks', json={
            'title': 'Test Task',
            'description': 'Test Description',
            'deadline': '2024-01-02T00:00:00',
            'priority': 'High',
            'status': 'Pending',
            'event_id': event_id,
            'assigned_to': 'testuser'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task created successfully', response.json['message'])

    def test_create_resource(self):
        # Register and login user first
        self.app.post('/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        login_response = self.app.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        token = login_response.json['token']
        
        # Create an event first
        self.app.post('/events', json={
            'title': 'Test Event',
            'date': '2024-01-01T00:00:00',
            'location': 'Test Location',
            'description': 'Test Description'
        }, headers={'Authorization': f'Bearer {token}'})
        
        event_id = Event.query.first().id

        response = self.app.post('/resources', json={
            'name': 'Test Resource',
            'type': 'Equipment',
            'status': 'Available',
            'event_id': event_id
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Resource created successfully', response.json['message'])

    def test_create_notification(self):
        # Register and login user first
        self.app.post('/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        login_response = self.app.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        token = login_response.json['token']
        
        response = self.app.post('/notifications', json={
            'title': 'Test Notification',
            'message': 'This is a test notification.'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Notification created successfully', response.json['message'])

if __name__ == '__main__':
    unittest.main()
