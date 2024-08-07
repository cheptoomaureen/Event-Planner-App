from app import app, db
from models import User, Event, Task, Resource, Expense, Notification
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

# Create all tables
with app.app_context():
    db.create_all()

    # Helper function to add and commit data
    def add_and_commit(session, instances):
        try:
            session.add_all(instances)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")

    # Clear existing data
    Notification.query.delete()
    Expense.query.delete()
    Resource.query.delete()
    Task.query.delete()
    Event.query.delete()
    User.query.delete()
    db.session.commit()

    # Users
    users = [
        User(username='user1', email='user1@example.com', password=generate_password_hash('password1')),
        User(username='user2', email='user2@example.com', password=generate_password_hash('password2')),
        User(username='user3', email='user3@example.com', password=generate_password_hash('password3')),
        User(username='user4', email='user4@example.com', password=generate_password_hash('password4')),
        User(username='user5', email='user5@example.com', password=generate_password_hash('password5'))
    ]
    
    add_and_commit(db.session, users)

    # Events
    events = [
        Event(title='Event 1', date=datetime.now() + timedelta(days=10), location='New York', description='Description for Event 1', created_by=1),
        Event(title='Event 2', date=datetime.now() + timedelta(days=15), location='San Francisco', description='Description for Event 2', created_by=2),
        Event(title='Event 3', date=datetime.now() + timedelta(days=20), location='Los Angeles', description='Description for Event 3', created_by=3),
        Event(title='Event 4', date=datetime.now() + timedelta(days=25), location='Chicago', description='Description for Event 4', created_by=4),
        Event(title='Event 5', date=datetime.now() + timedelta(days=30), location='Miami', description='Description for Event 5', created_by=5)
    ]

    add_and_commit(db.session, events)

    # Tasks
    tasks = [
        Task(title='Task 1', description='Task 1 Description', deadline=datetime.now() + timedelta(days=5), priority='High', status='Pending', event_id=1, assigned_to=1),
        Task(title='Task 2', description='Task 2 Description', deadline=datetime.now() + timedelta(days=6), priority='Medium', status='Pending', event_id=2, assigned_to=2),
        Task(title='Task 3', description='Task 3 Description', deadline=datetime.now() + timedelta(days=7), priority='Low', status='Pending', event_id=3, assigned_to=3),
        Task(title='Task 4', description='Task 4 Description', deadline=datetime.now() + timedelta(days=8), priority='Medium', status='Pending', event_id=4, assigned_to=4),
        Task(title='Task 5', description='Task 5 Description', deadline=datetime.now() + timedelta(days=9), priority='High', status='Pending', event_id=5, assigned_to=5)
    ]

    add_and_commit(db.session, tasks)

    # Resources
    resources = [
        Resource(name='Resource 1', type='Venue', status='Available', event_id=1),
        Resource(name='Resource 2', type='Equipment', status='Reserved', event_id=2, reserved_by='user2@example.com'),
        Resource(name='Resource 3', type='Catering', status='Available', event_id=3),
        Resource(name='Resource 4', type='Staff', status='Reserved', event_id=4, reserved_by='user4@example.com'),
        Resource(name='Resource 5', type='Venue', status='Available', event_id=5)
    ]

    add_and_commit(db.session, resources)

    # Expenses
    expenses = [
        Expense(amount=100.50, description='Expense 1 Description', event_id=1),
        Expense(amount=200.75, description='Expense 2 Description', event_id=2),
        Expense(amount=300.25, description='Expense 3 Description', event_id=3),
        Expense(amount=400.00, description='Expense 4 Description', event_id=4),
        Expense(amount=500.50, description='Expense 5 Description', event_id=5)
    ]

    add_and_commit(db.session, expenses)

    # Notifications
    notifications = [
        Notification(title='Notification 1', message='Message for Notification 1', user_id=1, created_at=datetime.now()),
        Notification(title='Notification 2', message='Message for Notification 2', user_id=2, created_at=datetime.now()),
        Notification(title='Notification 3', message='Message for Notification 3', user_id=3, created_at=datetime.now()),
        Notification(title='Notification 4', message='Message for Notification 4', user_id=4, created_at=datetime.now()),
        Notification(title='Notification 5', message='Message for Notification 5', user_id=5, created_at=datetime.now())
    ]

    add_and_commit(db.session, notifications)

    print("Database seeded!")
