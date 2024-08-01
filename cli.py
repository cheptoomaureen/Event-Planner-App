import sys
from app import app, db
from models import User, Event, Task, Resource, Expense
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

def show_users():
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f'{user.id}: {user.username} ({user.email})')

def create_user():
    with app.app_context():
        username = input('Username: ')
        email = input('Email: ')
        password = input('Password: ')
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print(f'User {username} created successfully.')

def update_user():
    with app.app_context():
        user_id = int(input('Enter User ID to update: '))
        user = User.query.get(user_id)
        if not user:
            print('User not found.')
            return
        username = input(f'New Username (leave blank to keep "{user.username}"): ')
        email = input(f'New Email (leave blank to keep "{user.email}"): ')
        password = input('New Password (leave blank to keep existing): ')
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = generate_password_hash(password)
        db.session.commit()
        print(f'User {user_id} updated successfully.')

def delete_user():
    with app.app_context():
        user_id = int(input("Enter User ID to delete: "))
        user = User.query.get(user_id)
        if user:
            events = Event.query.filter_by(creator_id=user_id).all()
            for event in events:
                Expense.query.filter_by(event_id=event.id).delete()
                Task.query.filter_by(event_id=event.id).delete()
                Resource.query.filter_by(event_id=event.id).delete()
                db.session.delete(event)
            Task.query.filter_by(assignee_id=user_id).delete()
            db.session.delete(user)
            db.session.commit()
            print(f"User ID {user_id} and related records have been deleted.")
        else:
            print(f"No user found with ID {user_id}.")

def show_events():
    with app.app_context():
        events = Event.query.all()
        for event in events:
            print(f'{event.id}: {event.title} on {event.date} at {event.location}')

def create_event():
    with app.app_context():
        title = input('Title: ')
        date_str = input('Date (YYYY-MM-DD HH:MM:SS): ')
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        location = input('Location: ')
        description = input('Description: ')
        creator_id = int(input('Creator ID: '))
        new_event = Event(title=title, date=date, location=location, description=description, created_by=creator_id)
        db.session.add(new_event)
        db.session.commit()
        print(f'Event {title} created successfully.')

def update_event():
    with app.app_context():
        event_id = int(input('Enter Event ID to update: '))
        event = Event.query.get(event_id)
        if not event:
            print('Event not found.')
            return
        title = input(f'New Title (leave blank to keep "{event.title}"): ')
        date_str = input(f'New Date (leave blank to keep "{event.date}"): ')
        location = input(f'New Location (leave blank to keep "{event.location}"): ')
        description = input(f'New Description (leave blank to keep "{event.description}"): ')
        if title:
            event.title = title
        if date_str:
            try:
                event.date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print('Invalid date format.')
                return
        if location:
            event.location = location
        if description:
            event.description = description
        db.session.commit()
        print(f'Event {event_id} updated successfully.')

def delete_event():
    with app.app_context():
        event_id = int(input('Enter Event ID to delete: '))
        event = Event.query.get(event_id)
        if event:
            Expense.query.filter_by(event_id=event_id).delete()
            Task.query.filter_by(event_id=event_id).delete()
            Resource.query.filter_by(event_id=event_id).delete()
            db.session.delete(event)
            db.session.commit()
            print(f'Event {event_id} deleted successfully.')
        else:
            print('Event not found.')

def show_tasks():
    with app.app_context():
        tasks = Task.query.all()
        for task in tasks:
            print(f'{task.id}: {task.title} (Deadline: {task.deadline}, Priority: {task.priority}, Status: {task.status})')

def create_task():
    with app.app_context():
        title = input('Title: ')
        description = input('Description: ')
        deadline_str = input('Deadline (YYYY-MM-DD HH:MM:SS): ')
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
        priority = input('Priority: ')
        status = input('Status: ')
        event_id = int(input('Event ID: '))
        assignee_id = int(input('Assignee ID: '))
        new_task = Task(title=title, description=description, deadline=deadline, priority=priority, status=status, event_id=event_id, assigned_to=assignee_id)
        db.session.add(new_task)
        db.session.commit()
        print(f'Task {title} created successfully.')

def update_task():
    with app.app_context():
        task_id = int(input('Enter Task ID to update: '))
        task = Task.query.get(task_id)
        if not task:
            print('Task not found.')
            return
        title = input(f'New Title (leave blank to keep "{task.title}"): ')
        description = input(f'New Description (leave blank to keep "{task.description}"): ')
        deadline_str = input(f'New Deadline (leave blank to keep "{task.deadline}"): ')
        priority = input(f'New Priority (leave blank to keep "{task.priority}"): ')
        status = input(f'New Status (leave blank to keep "{task.status}"): ')
        if title:
            task.title = title
        if description:
            task.description = description
        if deadline_str:
            try:
                task.deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print('Invalid deadline format.')
                return
        if priority:
            task.priority = priority
        if status:
            task.status = status
        db.session.commit()
        print(f'Task {task_id} updated successfully.')

def delete_task():
    with app.app_context():
        task_id = int(input('Enter Task ID to delete: '))
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            print(f'Task {task_id} deleted successfully.')
        else:
            print('Task not found.')

def show_resources():
    with app.app_context():
        resources = Resource.query.all()
        for resource in resources:
            print(f'{resource.id}: {resource.name} (Type: {resource.type}, Status: {resource.status})')

def create_resource():
    with app.app_context():
        name = input('Name: ')
        type = input('Type: ')
        status = input('Status: ')
        event_id = int(input('Event ID: '))
        reserved_by_id = int(input('Reserved By ID: '))
        new_resource = Resource(name=name, type=type, status=status, event_id=event_id, reserved_by=reserved_by_id)
        db.session.add(new_resource)
        db.session.commit()
        print(f'Resource {name} created successfully.')

def update_resource():
    with app.app_context():
        resource_id = int(input('Enter Resource ID to update: '))
        resource = Resource.query.get(resource_id)
        if not resource:
            print('Resource not found.')
            return
        name = input(f'New Name (leave blank to keep "{resource.name}"): ')
        type = input(f'New Type (leave blank to keep "{resource.type}"): ')
        status = input(f'New Status (leave blank to keep "{resource.status}"): ')
        reserved_by_id = input(f'New Reserved By ID (leave blank to keep "{resource.reserved_by}"): ')
        if name:
            resource.name = name
        if type:
            resource.type = type
        if status:
            resource.status = status
        if reserved_by_id:
            resource.reserved_by = int(reserved_by_id)
        db.session.commit()
        print(f'Resource {resource_id} updated successfully.')

def delete_resource():
    with app.app_context():
        resource_id = int(input('Enter Resource ID to delete: '))
        resource = Resource.query.get(resource_id)
        if resource:
            db.session.delete(resource)
            db.session.commit()
            print(f'Resource {resource_id} deleted successfully.')
        else:
            print('Resource not found.')

def show_expenses():
    with app.app_context():
        expenses = Expense.query.all()
        for expense in expenses:
            print(f'{expense.id}: {expense.amount} ({expense.description})')

def create_expense():
    with app.app_context():
        amount = float(input('Amount: '))
        description = input('Description: ')
        event_id = int(input('Event ID: '))
        new_expense = Expense(amount=amount, description=description, event_id=event_id)
        db.session.add(new_expense)
        db.session.commit()
        print(f'Expense of {amount} created successfully.')

def update_expense():
    with app.app_context():
        expense_id = int(input('Enter Expense ID to update: '))
        expense = Expense.query.get(expense_id)
        if not expense:
            print('Expense not found.')
            return
        amount = input(f'New Amount (leave blank to keep "{expense.amount}"): ')
        description = input(f'New Description (leave blank to keep "{expense.description}"): ')
        if amount:
            expense.amount = float(amount)
        if description:
            expense.description = description
        db.session.commit()
        print(f'Expense {expense_id} updated successfully.')

def delete_expense():
    with app.app_context():
        expense_id = int(input('Enter Expense ID to delete: '))
        expense = Expense.query.get(expense_id)
        if expense:
            db.session.delete(expense)
            db.session.commit()
            print(f'Expense {expense_id} deleted successfully.')
        else:
            print('Expense not found.')

if __name__ == '__main__':
    while True:
        print("""
        1. Show Users
        2. Create User
        3. Update User
        4. Delete User
        5. Show Events
        6. Create Event
        7. Update Event
        8. Delete Event
        9. Show Tasks
        10. Create Task
        11. Update Task
        12. Delete Task
        13. Show Resources
        14. Create Resource
        15. Update Resource
        16. Delete Resource
        17. Show Expenses
        18. Create Expense
        19. Update Expense
        20. Delete Expense
        21. Exit
        """)
        choice = input('Enter choice: ')
        if choice == '1':
            show_users()
        elif choice == '2':
            create_user()
        elif choice == '3':
            update_user()
        elif choice == '4':
            delete_user()
        elif choice == '5':
            show_events()
        elif choice == '6':
            create_event()
        elif choice == '7':
            update_event()
        elif choice == '8':
            delete_event()
        elif choice == '9':
            show_tasks()
        elif choice == '10':
            create_task()
        elif choice == '11':
            update_task()
        elif choice == '12':
            delete_task()
        elif choice == '13':
            show_resources()
        elif choice == '14':
            create_resource()
        elif choice == '15':
            update_resource()
        elif choice == '16':
            delete_resource()
        elif choice == '17':
            show_expenses()
        elif choice == '18':
            create_expense()
        elif choice == '19':
            update_expense()
        elif choice == '20':
            delete_expense()
        elif choice == '21':
            sys.exit()
        else:
            print('Invalid choice. Please try again.')
