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
        User(username='john_doe', email='john@example.com', password=generate_password_hash('password123')),
        User(username='jane_smith', email='jane@example.com', password=generate_password_hash('password456')),
        User(username='michael_brown', email='michael@example.com', password=generate_password_hash('password789')),
        User(username='sarah_connor', email='sarah@example.com', password=generate_password_hash('password101')),
        User(username='chris_evans', email='chris@example.com', password=generate_password_hash('password202')),
        User(username='tony_stark', email='tony@example.com', password=generate_password_hash('ironman')),
        User(username='natasha_romanoff', email='natasha@example.com', password=generate_password_hash('blackwidow')),
        User(username='bruce_banner', email='bruce@example.com', password=generate_password_hash('hulk')),
        User(username='steve_rogers', email='steve@example.com', password=generate_password_hash('capamerica')),
        User(username='peter_parker', email='peter@example.com', password=generate_password_hash('spiderman')),
        User(username='clark_kent', email='clark@example.com', password=generate_password_hash('superman')),
        User(username='diana_prince', email='diana@example.com', password=generate_password_hash('wonderwoman')),
        User(username='bruce_wayne', email='bruce.wayne@example.com', password=generate_password_hash('batman')),
        User(username='barry_allen', email='barry@example.com', password=generate_password_hash('flash')),
        User(username='arthur_curry', email='arthur@example.com', password=generate_password_hash('aquaman'))
    ]
    
    add_and_commit(db.session, users)

    # Events
    events = [
        Event(title='Tech Conference 2024', date=datetime.now() + timedelta(days=30), location='San Francisco, CA', description='A tech conference focused on AI advancements.', created_by=1),
        Event(title='Marketing Summit', date=datetime.now() + timedelta(days=45), location='New York, NY', description='An annual summit for marketing professionals.', created_by=2),
        Event(title='Startup Pitch', date=datetime.now() + timedelta(days=60), location='Los Angeles, CA', description='A platform for startups to pitch their ideas to investors.', created_by=3),
        Event(title='Developer Bootcamp', date=datetime.now() + timedelta(days=75), location='Austin, TX', description='A 10-day bootcamp for aspiring developers.', created_by=4),
        Event(title='Cybersecurity Workshop', date=datetime.now() + timedelta(days=90), location='Chicago, IL', description='A workshop on the latest trends in cybersecurity.', created_by=5),
        Event(title='Product Launch', date=datetime.now() + timedelta(days=20), location='Seattle, WA', description='Launch event for our new product line.', created_by=6),
        Event(title='Annual Company Meeting', date=datetime.now() + timedelta(days=35), location='Miami, FL', description='Yearly meeting for all company employees.', created_by=7),
        Event(title='Healthcare Expo', date=datetime.now() + timedelta(days=50), location='Orlando, FL', description='Expo showcasing the latest in healthcare technology.', created_by=8),
        Event(title='Renewable Energy Symposium', date=datetime.now() + timedelta(days=65), location='Denver, CO', description='A symposium on the future of renewable energy.', created_by=9),
        Event(title='Gaming Convention', date=datetime.now() + timedelta(days=80), location='Las Vegas, NV', description='Convention for the gaming industry.', created_by=10),
        Event(title='Financial Planning Workshop', date=datetime.now() + timedelta(days=95), location='Boston, MA', description='Workshop on personal financial planning.', created_by=11),
        Event(title='Art and Design Exhibition', date=datetime.now() + timedelta(days=110), location='San Diego, CA', description='Exhibition featuring works from contemporary artists.', created_by=12),
        Event(title='Non-Profit Fundraiser', date=datetime.now() + timedelta(days=125), location='Washington, D.C.', description='Fundraiser event for our non-profit partners.', created_by=13),
        Event(title='Tech Hiring Fair', date=datetime.now() + timedelta(days=140), location='Atlanta, GA', description='A hiring fair for tech companies and professionals.', created_by=14),
        Event(title='Music Festival', date=datetime.now() + timedelta(days=155), location='Nashville, TN', description='Annual music festival featuring top artists.', created_by=15)
    ]

    add_and_commit(db.session, events)

    # Tasks
    tasks = [
        Task(title='Book Venue', description='Book the venue for the Tech Conference 2024.', deadline=datetime.now() + timedelta(days=10), priority='High', status='Pending', event_id=1, assigned_to=1),
        Task(title='Send Invitations', description='Send out invitations to all potential attendees.', deadline=datetime.now() + timedelta(days=12), priority='Medium', status='Pending', event_id=2, assigned_to=2),
        Task(title='Prepare Marketing Materials', description='Create and print marketing materials for the summit.', deadline=datetime.now() + timedelta(days=14), priority='High', status='In Progress', event_id=3, assigned_to=3),
        Task(title='Coordinate with Speakers', description='Ensure all speakers are confirmed and briefed.', deadline=datetime.now() + timedelta(days=16), priority='High', status='In Progress', event_id=4, assigned_to=4),
        Task(title='Arrange Catering', description='Arrange catering services for the bootcamp.', deadline=datetime.now() + timedelta(days=18), priority='Medium', status='Pending', event_id=5, assigned_to=5),
        Task(title='Secure Sponsors', description='Contact and secure sponsorships for the event.', deadline=datetime.now() + timedelta(days=20), priority='High', status='Pending', event_id=6, assigned_to=6),
        Task(title='Design Stage Setup', description='Design the stage setup for the product launch.', deadline=datetime.now() + timedelta(days=22), priority='Medium', status='Pending', event_id=7, assigned_to=7),
        Task(title='Organize Transportation', description='Arrange transportation for all VIP attendees.', deadline=datetime.now() + timedelta(days=24), priority='Low', status='Pending', event_id=8, assigned_to=8),
        Task(title='Finalize Event Schedule', description='Finalize the schedule and distribute to attendees.', deadline=datetime.now() + timedelta(days=26), priority='High', status='In Progress', event_id=9, assigned_to=9),
        Task(title='Print Name Badges', description='Print and prepare name badges for all attendees.', deadline=datetime.now() + timedelta(days=28), priority='Low', status='Completed', event_id=10, assigned_to=10),
        Task(title='Review AV Requirements', description='Review and confirm all audio-visual requirements.', deadline=datetime.now() + timedelta(days=30), priority='Medium', status='Pending', event_id=11, assigned_to=11),
        Task(title='Hire Security', description='Hire security personnel for the event.', deadline=datetime.now() + timedelta(days=32), priority='High', status='In Progress', event_id=12, assigned_to=12),
        Task(title='Distribute Press Kits', description='Prepare and distribute press kits to media.', deadline=datetime.now() + timedelta(days=34), priority='Medium', status='Pending', event_id=13, assigned_to=13),
        Task(title='Arrange Entertainment', description='Book entertainment for the fundraiser event.', deadline=datetime.now() + timedelta(days=36), priority='Low', status='Pending', event_id=14, assigned_to=14),
        Task(title='Prepare Budget Report', description='Prepare a detailed budget report for the event.', deadline=datetime.now() + timedelta(days=38), priority='High', status='Pending', event_id=15, assigned_to=15)
    ]

    add_and_commit(db.session, tasks)

    # Resources
    resources = [
        Resource(name='Main Auditorium', type='Venue', status='Reserved', event_id=1, reserved_by='john@example.com'),
        Resource(name='Projector', type='Equipment', status='Available', event_id=2),
        Resource(name='Keynote Speaker', type='Speaker', status='Confirmed', event_id=3, reserved_by='jane@example.com'),
        Resource(name='Catering Service', type='Catering', status='Reserved', event_id=4, reserved_by='michael@example.com'),
        Resource(name='Security Team', type='Staff', status='Reserved', event_id=5, reserved_by='sarah@example.com'),
        Resource(name='VIP Lounge', type='Venue', status='Available', event_id=6),
        Resource(name='Sound System', type='Equipment', status='Available', event_id=7),
        Resource(name='Stage Lighting', type='Equipment', status='Reserved', event_id=8, reserved_by='chris@example.com'),
        Resource(name='Marketing Materials', type='Printed Materials', status='Delivered', event_id=9),
        Resource(name='Media Kit', type='Printed Materials', status='In Production', event_id=10),
        Resource(name='Catering Staff', type='Staff', status='Reserved', event_id=11, reserved_by='tony@example.com'),
        Resource(name='Event Photographer', type='Staff', status='Available', event_id=12),
        Resource(name='Conference Room', type='Venue', status='Reserved', event_id=13, reserved_by='natasha@example.com'),
        Resource(name='Audio-Visual Team', type='Staff', status='Available', event_id=14),
        Resource(name='Public Relations Firm', type='Service', status='Hired', event_id=15)
    ]

    add_and_commit(db.session, resources)

    # Expenses
    expenses = [
        Expense(amount=5000.00, description='Venue rental for the Tech Conference 2024.', event_id=1),
        Expense(amount=2500.00, description='Marketing materials and promotions.', event_id=2),
        Expense(amount=7500.00, description='Speaker fees and travel expenses.', event_id=3),
        Expense(amount=3000.00, description='Catering for the Developer Bootcamp.', event_id=4),
        Expense(amount=1200.00, description='Security services for the event.', event_id=5),
        Expense(amount=4000.00, description='Stage design and setup for the product launch.', event_id=6),
        Expense(amount=1500.00, description='Transportation for VIP attendees.', event_id=7),
        Expense(amount=500.00, description='Name badge printing costs.', event_id=8),
        Expense(amount=1000.00, description='AV equipment rental.', event_id=9),
        Expense(amount=800.00, description='Press kit production.', event_id=10),
        Expense(amount=4500.00, description='Security personnel fees.', event_id=11),
        Expense(amount=3500.00, description='Event photographer and media coverage.', event_id=12),
        Expense(amount=2000.00, description='Conference room rental for the fundraiser.', event_id=13),
        Expense(amount=2500.00, description='Audio-visual team services.', event_id=14),
        Expense(amount=5500.00, description='Public relations services for the event.', event_id=15)
    ]

    add_and_commit(db.session, expenses)

    # Notifications
    notifications = [
        Notification(title='Venue Reserved', message='The venue for Tech Conference 2024 has been successfully reserved.', user_id=1, created_at=datetime.now()),
        Notification(title='Marketing Materials Approved', message='All marketing materials have been approved and sent for printing.', user_id=2, created_at=datetime.now()),
        Notification(title='Speaker Confirmed', message='The keynote speaker for Startup Pitch has confirmed.', user_id=3, created_at=datetime.now()),
        Notification(title='Catering Service Reserved', message='Catering services for the bootcamp have been reserved.', user_id=4, created_at=datetime.now()),
        Notification(title='Security Team Hired', message='Security team has been hired for the Cybersecurity Workshop.', user_id=5, created_at=datetime.now()),
        Notification(title='Product Launch Stage Design', message='Stage design for the product launch has been finalized.', user_id=6, created_at=datetime.now()),
        Notification(title='Transportation Arranged', message='Transportation for VIP attendees has been arranged.', user_id=7, created_at=datetime.now()),
        Notification(title='Event Schedule Finalized', message='The event schedule has been finalized and distributed.', user_id=8, created_at=datetime.now()),
        Notification(title='Name Badges Printed', message='Name badges have been printed and are ready for distribution.', user_id=9, created_at=datetime.now()),
        Notification(title='AV Requirements Confirmed', message='All audio-visual requirements have been confirmed.', user_id=10, created_at=datetime.now()),
        Notification(title='Security Hired', message='Security personnel have been hired for the Art and Design Exhibition.', user_id=11, created_at=datetime.now()),
        Notification(title='Photographer Booked', message='Photographer for the event has been booked.', user_id=12, created_at=datetime.now()),
        Notification(title='Press Kits Distributed', message='Press kits have been distributed to the media.', user_id=13, created_at=datetime.now()),
        Notification(title='Entertainment Arranged', message='Entertainment for the fundraiser has been arranged.', user_id=14, created_at=datetime.now()),
        Notification(title='Budget Report Ready', message='The budget report for the event is ready for review.', user_id=15, created_at=datetime.now())
    ]

    add_and_commit(db.session, notifications)

    print("Database seeded!")
