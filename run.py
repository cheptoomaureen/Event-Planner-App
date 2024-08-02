from app import app, db
from models import User, Event, Task, Resource, Expense, Notification
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_sample_data():
    with app.app_context():
        db.create_all()  # Create database tables

        # Check if users already exist
        existing_user1 = User.query.filter_by(email="john@example.com").first()
        existing_user2 = User.query.filter_by(email="jane@example.com").first()

        if not existing_user1:
            user1 = User(
                username="john_doe",
                email="john@example.com",
                password=generate_password_hash("password123", method='pbkdf2:sha256')
            )
            db.session.add(user1)

        if not existing_user2:
            user2 = User(
                username="jane_doe",
                email="jane@example.com",
                password=generate_password_hash("password123", method='pbkdf2:sha256')
            )
            db.session.add(user2)

        db.session.commit()

        # Fetch the user ids after committing
        user1 = existing_user1 if existing_user1 else User.query.filter_by(email="john@example.com").first()
        user2 = existing_user2 if existing_user2 else User.query.filter_by(email="jane@example.com").first()

        # Create Events
        event1 = Event(
            title="John's Birthday Party",
            date=datetime.strptime("2024-08-15T18:00:00", '%Y-%m-%dT%H:%M:%S'),
            location="John's House",
            description="A fun birthday party for John!",
            created_by=user1.id
        )
        event2 = Event(
            title="Jane's Wedding",
            date=datetime.strptime("2024-09-30T12:00:00", '%Y-%m-%dT%H:%M:%S'),
            location="Beach Resort",
            description="A beautiful beach wedding for Jane.",
            created_by=user2.id
        )

        db.session.add(event1)
        db.session.add(event2)
        db.session.commit()

        # Create Tasks
        task1 = Task(
            title="Buy Cake",
            description="Order the cake from the bakery",
            deadline=datetime.strptime("2024-08-14T15:00:00", '%Y-%m-%dT%H:%M:%S'),
            priority="High",
            status="Pending",
            event_id=event1.id,
            assigned_to="john_doe"
        )
        task2 = Task(
            title="Send Invitations",
            description="Send out wedding invitations to all guests",
            deadline=datetime.strptime("2024-09-10T10:00:00", '%Y-%m-%dT%H:%M:%S'),
            priority="Medium",
            status="Completed",
            event_id=event2.id,
            assigned_to="jane_doe"
        )

        db.session.add(task1)
        db.session.add(task2)
        db.session.commit()

        # Create Resources
        resource1 = Resource(
            name="Birthday Cake",
            type="Food",
            status="Ordered",
            event_id=event1.id,
            reserved_by="john_doe"
        )
        resource2 = Resource(
            name="Beach Venue",
            type="Location",
            status="Booked",
            event_id=event2.id,
            reserved_by="jane_doe"
        )

        db.session.add(resource1)
        db.session.add(resource2)
        db.session.commit()

        # Create Expenses
        expense1 = Expense(
            amount=150.00,
            description="Birthday Cake",
            event_id=event1.id
        )
        expense2 = Expense(
            amount=2000.00,
            description="Wedding Venue",
            event_id=event2.id
        )

        db.session.add(expense1)
        db.session.add(expense2)
        db.session.commit()

        # Create Notifications
        notification1 = Notification(
            title="Task Reminder",
            message="Don't forget to buy the cake for John's birthday.",
            user_id=user1.id,
            created_at=datetime.utcnow()
        )
        notification2 = Notification(
            title="Wedding Update",
            message="The wedding venue has been booked successfully.",
            user_id=user2.id,
            created_at=datetime.utcnow()
        )

        db.session.add(notification1)
        db.session.add(notification2)
        db.session.commit()

        print("Sample data created successfully!")

if __name__ == "__main__":
    create_sample_data()
