import sys
from app import app, db
from models import User, Event, Task, Resource, Expense
from werkzeug.security import generate_password_hash
from datetime import datetime

DEFAULT_USER_ID = 1  # Change this to the actual user ID in your database

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
        try:
            user_id = int(input('Enter User ID to update: '))
        except ValueError:
            print("Invalid User ID. It must be a number.")
            return

        user = db.session.get(User, user_id)
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
        try:
            user_id = int(input('Enter User ID to delete: '))
        except ValueError:
            print("Invalid User ID. It must be a number.")
            return

        user = db.session.get(User, user_id)
        if not user:
            print('User not found.')
            return

        # Reassign events to the default user
        events = Event.query.filter_by(creator_id=user_id).all()
        for event in events:
            event.creator_id = DEFAULT_USER_ID

        db.session.delete(user)
        try:
            db.session.commit()
            print(f'User {user_id} deleted successfully and events reassigned to default user.')
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")

def show_events():
    with app.app_context():
        events = Event.query.all()
        for event in events:
            print(f'{event.id}: {event.title} on {event.date} at {event.location}')

def create_event():
    with app.app_context():
        title = input('Title: ')
        date_str = input('Date (YYYY-MM-DD HH:MM:SS): ')
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            print('Invalid date format.')
            return
        location = input('Location: ')
        description = input('Description: ')
        try:
            creator_id = int(input('Creator ID: '))
        except ValueError:
            print("Invalid Creator ID. It must be a number.")
            return

        new_event = Event(title=title, date=date, location=location, description=description, created_by=creator_id)
        db.session.add(new_event)
        db.session.commit()
        print(f'Event {title} created successfully.')

def update_event():
    with app.app_context():
        try:
            event_id = int(input('Enter Event ID to update: '))
        except ValueError:
            print("Invalid Event ID. It must be a number.")
            return

        event = db.session.get(Event, event_id)
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
        try:
            event_id = int(input('Enter Event ID to delete: '))
        except ValueError:
            print("Invalid Event ID. It must be a number.")
            return

        event = db.session.get(Event, event_id)
        if not event:
            print('Event not found.')
            return

        db.session.delete(event)
        db.session.commit()
        print(f'Event {event_id} deleted successfully.')

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
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            print('Invalid deadline format.')
            return
        priority = input('Priority: ')
        status = input('Status: ')
        try:
            event_id = int(input('Event ID: '))
            assignee_id = int(input('Assignee ID: '))
        except ValueError:
            print("Invalid ID. Both Event ID and Assignee ID must be numbers.")
            return

        new_task = Task(title=title, description=description, deadline=deadline, priority=priority, status=status, event_id=event_id, assigned_to=assignee_id)
        db.session.add(new_task)
        db.session.commit()
        print(f'Task {title} created successfully.')

def update_task():
    with app.app_context():
        try:
            task_id = int(input('Enter Task ID to update: '))
        except ValueError:
            print("Invalid Task ID. It must be a number.")
            return

        task = db.session.get(Task, task_id)
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
        try:
            task_id = int(input('Enter Task ID to delete: '))
        except ValueError:
            print("Invalid Task ID. It must be a number.")
            return

        task = db.session.get(Task, task_id)
        if not task:
            print('Task not found.')
            return

        db.session.delete(task)
        db.session.commit()
        print(f'Task {task_id} deleted successfully.')
        
def show_resources():
    with app.app_context():
        resources = Resource.query.all()
        for resource in resources:
            # Adjust the fields according to the actual Resource model
            print(f'{resource.id}: {resource.name} (Description: {resource.description}, Status: {resource.status})')

def create_resource():
    with app.app_context():
        name = input('Name: ')
        description = input('Description: ')
        status = input('Status: ')  # Assuming you have a status field
        try:
            event_id = int(input('Event ID: '))
        except ValueError:
            print("Invalid Event ID. It must be a number.")
            return

        new_resource = Resource(name=name, description=description, status=status, event_id=event_id)
        db.session.add(new_resource)
        db.session.commit()
        print(f'Resource {name} created successfully.')

def update_resource():
    with app.app_context():
        try:
            resource_id = int(input('Enter Resource ID to update: '))
        except ValueError:
            print("Invalid Resource ID. It must be a number.")
            return

        resource = db.session.get(Resource, resource_id)
        if not resource:
            print('Resource not found.')
            return

        name = input(f'New Name (leave blank to keep "{resource.name}"): ')
        description = input(f'New Description (leave blank to keep "{resource.description}"): ')
        status = input(f'New Status (leave blank to keep "{resource.status}"): ')

        if name:
            resource.name = name
        if description:
            resource.description = description
        if status:
            resource.status = status

        db.session.commit()
        print(f'Resource {resource_id} updated successfully.')

def delete_resource():
    with app.app_context():
        try:
            resource_id = int(input('Enter Resource ID to delete: '))
        except ValueError:
            print("Invalid Resource ID. It must be a number.")
            return

        resource = db.session.get(Resource, resource_id)
        if not resource:
            print('Resource not found.')
            return

        db.session.delete(resource)
        db.session.commit()
        print(f'Resource {resource_id} deleted successfully.')


def show_expenses():
    with app.app_context():
        expenses = Expense.query.all()
        for expense in expenses:
            print(f'{expense.id}: Amount {expense.amount} (Name: {expense.name})')

def create_expense():
    with app.app_context():
        try:
            amount = float(input('Amount: '))
        except ValueError:
            print("Invalid amount. It must be a number.")
            return

        name = input('Name: ')
        try:
            event_id = int(input('Event ID: '))
        except ValueError:
            print("Invalid Event ID. It must be a number.")
            return

        new_expense = Expense(amount=amount, name=name, event_id=event_id)
        db.session.add(new_expense)
        db.session.commit()
        print(f'Expense of {amount} created successfully.')

def update_expense():
    with app.app_context():
        try:
            expense_id = int(input('Enter Expense ID to update: '))
        except ValueError:
            print("Invalid Expense ID. It must be a number.")
            return

        expense = db.session.get(Expense, expense_id)
        if not expense:
            print('Expense not found.')
            return

        amount = input(f'New Amount (leave blank to keep "{expense.amount}"): ')
        name = input(f'New Name (leave blank to keep "{expense.name}"): ')

        if amount:
            try:
                expense.amount = float(amount)
            except ValueError:
                print("Invalid amount. It must be a number.")
                return
        if name:
            expense.name = name

        db.session.commit()
        print(f'Expense {expense_id} updated successfully.')

def delete_expense():
    with app.app_context():
        try:
            expense_id = int(input('Enter Expense ID to delete: '))
        except ValueError:
            print("Invalid Expense ID. It must be a number.")
            return

        expense = db.session.get(Expense, expense_id)
        if not expense:
            print('Expense not found.')
            return

        db.session.delete(expense)
        db.session.commit()
        print(f'Expense {expense_id} deleted successfully.')

def select_class_action():
    print("Select a class to perform CRUD operations on:")
    print("1. Users")
    print("2. Events")
    print("3. Tasks")
    print("4. Resources")
    print("5. Expenses")
    choice = input("Enter the number of your choice: ")

    if choice == '1':
        manage_users()
    elif choice == '2':
        manage_events()
    elif choice == '3':
        manage_tasks()
    elif choice == '4':
        manage_resources()
    elif choice == '5':
        manage_expenses()
    else:
        print("Invalid choice.")
        sys.exit(1)

def manage_users():
    print("User Operations:")
    print("1. Show all users")
    print("2. Create a new user")
    print("3. Update a user")
    print("4. Delete a user")
    choice = input("Enter the number of your choice: ")
    if choice == '1':
        show_users()
    elif choice == '2':
        create_user()
    elif choice == '3':
        update_user()
    elif choice == '4':
        delete_user()
    else:
        print("Invalid choice.")
        sys.exit(1)

def manage_events():
    print("Event Operations:")
    print("1. Show all events")
    print("2. Create a new event")
    print("3. Update an event")
    print("4. Delete an event")
    choice = input("Enter the number of your choice: ")
    if choice == '1':
        show_events()
    elif choice == '2':
        create_event()
    elif choice == '3':
        update_event()
    elif choice == '4':
        delete_event()
    else:
        print("Invalid choice.")
        sys.exit(1)

def manage_tasks():
    print("Task Operations:")
    print("1. Show all tasks")
    print("2. Create a new task")
    print("3. Update a task")
    print("4. Delete a task")
    choice = input("Enter the number of your choice: ")
    if choice == '1':
        show_tasks()
    elif choice == '2':
        create_task()
    elif choice == '3':
        update_task()
    elif choice == '4':
        delete_task()
    else:
        print("Invalid choice.")
        sys.exit(1)

def manage_resources():
    print("Resource Operations:")
    print("1. Show all resources")
    print("2. Create a new resource")
    print("3. Update a resource")
    print("4. Delete a resource")
    choice = input("Enter the number of your choice: ")
    if choice == '1':
        show_resources()
    elif choice == '2':
        create_resource()
    elif choice == '3':
        update_resource()
    elif choice == '4':
        delete_resource()
    else:
        print("Invalid choice.")
        sys.exit(1)

def manage_expenses():
    print("Expense Operations:")
    print("1. Show all expenses")
    print("2. Create a new expense")
    print("3. Update an expense")
    print("4. Delete an expense")
    choice = input("Enter the number of your choice: ")
    if choice == '1':
        show_expenses()
    elif choice == '2':
        create_expense()
    elif choice == '3':
        update_expense()
    elif choice == '4':
        delete_expense()
    else:
        print("Invalid choice.")
        sys.exit(1)

def main():
    """Main function to handle CLI commands"""
    if len(sys.argv) < 2:
        select_class_action()
    else:
        command = sys.argv[1]
        commands = {
            'show_users': show_users,
            'create_user': create_user,
            'update_user': update_user,
            'delete_user': delete_user,
            'show_events': show_events,
            'create_event': create_event,
            'update_event': update_event,
            'delete_event': delete_event,
            'show_tasks': show_tasks,
            'create_task': create_task,
            'update_task': update_task,
            'delete_task': delete_task,
            'show_resources': show_resources,
            'create_resource': create_resource,
            'update_resource': update_resource,
            'delete_resource': delete_resource,
            'show_expenses': show_expenses,
            'create_expense': create_expense,
            'update_expense': update_expense,
            'delete_expense': delete_expense,
        }
        if command in commands:
            commands[command]()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: " + ", ".join(commands.keys()))
            sys.exit(1)

if __name__ == "__main__":
    main()
