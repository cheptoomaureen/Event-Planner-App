import logging
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_cors import CORS
from models import db, User, Event, Task, Resource, Expense, Notification
from datetime import timedelta, datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your_jwt_secret_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your_secret_key")

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)

app.logger.info('App startup')

@app.route("/")
def index():
    app.logger.info('Index page accessed')
    return "<h1>Event Planner</h1>"

@app.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode("utf-8")
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    app.logger.info(f"User registered: {new_user.username}")
    return jsonify({'message': 'User registered successfully'})

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id)
        app.logger.info(f"User logged in: {user.username}")
        return jsonify({'token': token})
    app.logger.warning(f'Failed login attempt for {data["email"]}')
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route("/auth/current_user", methods=["GET"])
@jwt_required(optional=True)
def get_current_user():
    current_user_id = get_jwt_identity()
    if current_user_id:
        current_user = User.query.get(current_user_id)
        if current_user:
            app.logger.info(f'Current user {current_user.email} fetched')
            return jsonify({"id": current_user.id, "username": current_user.username, "email": current_user.email}), 200
    app.logger.warning('User not found')
    return jsonify({"error": "User not found"}), 404

BLACKLIST = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@app.route("/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLACKLIST.add(jti)
    app.logger.info('User logged out')
    return jsonify({"success": "Successfully logged out"}), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=bcrypt.generate_password_hash(data['password']).decode("utf-8"))
    db.session.add(new_user)
    db.session.commit()
    app.logger.info(f'User {new_user.email} created successfully')
    return jsonify({'success': 'User created successfully'}), 201

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    app.logger.info('Fetched all users')
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email
    } for user in users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    app.logger.info(f'User {user.email} fetched')
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@app.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required(optional=True)
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password']).decode("utf-8")

    db.session.commit()
    app.logger.info(f'User {user.email} updated successfully')
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    app.logger.info(f'User {user.email} deleted')
    return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/events', methods=['POST'])
@jwt_required(optional=True)
def create_event():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    try:
        event_date = datetime.fromisoformat(data['date'])
    except ValueError:
        app.logger.warning('Invalid date format')
        return jsonify({'message': 'Invalid date format. Use ISO 8601 format.'}), 400

    new_event = Event(
        title=data['title'],
        date=event_date,
        location=data['location'],
        description=data.get('description', ''),
        created_by=current_user_id
    )

    db.session.add(new_event)
    db.session.commit()
    app.logger.info(f'Event {new_event.title} created successfully')
    return jsonify({'message': 'Event created successfully'}), 201

@app.route('/events', methods=['GET'])
@jwt_required(optional=True)
def get_all_events():
    events = Event.query.all()
    app.logger.info('Fetched all events')
    return jsonify([
        {
            'id': event.id,
            'title': event.title,
            'date': event.date.isoformat(),
            'location': event.location,
            'description': event.description
        }
        for event in events
    ]), 200

@app.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get_or_404(id)
    app.logger.info(f'Event {event.title} fetched')
    return jsonify({
        'id': event.id,
        'title': event.title,
        'date': event.date.isoformat(),
        'location': event.location,
        'description': event.description
    }), 200

@app.route('/events/<int:id>', methods=['PUT'])
@jwt_required(optional=True)
def update_event(id):
    data = request.get_json()
    event = Event.query.get_or_404(id)

    event.title = data.get('title', event.title)
    try:
        event.date = datetime.fromisoformat(data.get('date', event.date.isoformat()))
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use ISO 8601 format.'}), 400
    event.location = data.get('location', event.location)
    event.description = data.get('description', event.description)

    db.session.commit()
    app.logger.info(f'Event {event.title} updated successfully')
    return jsonify({'message': 'Event updated successfully'}), 200

@app.route('/events/<int:id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    app.logger.info(f'Event {event.title} deleted')
    return jsonify({'message': 'Event deleted successfully'}), 200

@app.route('/tasks', methods=['POST'])
@jwt_required(optional=True)
def create_task():
    data = request.get_json()
    try:
        deadline = datetime.fromisoformat(data['deadline'])
    except ValueError:
        return jsonify({'message': 'Invalid datetime format. Use ISO 8601 format.'}), 400

    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        deadline=deadline,
        priority=data['priority'],
        status=data.get('status', 'Pending'),
        event_id=data['event_id'],
        assigned_to=data['assigned_to']
    )
    db.session.add(new_task)
    db.session.commit()
    app.logger.info(f"Task {new_task.title} created successfully")
    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/tasks', methods=['GET'])
@jwt_required(optional=True)
def get_all_tasks():
    tasks = Task.query.all()
    app.logger.info('Fetched all tasks')
    return jsonify([
        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'deadline': task.deadline.isoformat(),
            'priority': task.priority,
            'status': task.status,
            'event_id': task.event_id,
            'assigned_to': task.assigned_to
        }
        for task in tasks
    ]), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    app.logger.info(f'Task {task.title} fetched')
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'deadline': task.deadline.isoformat(),
        'priority': task.priority,
        'status': task.status,
        'event_id': task.event_id,
        'assigned_to': task.assigned_to
    }), 200

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required(optional=True)
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get_or_404(task_id)
    try:
        task.deadline = datetime.fromisoformat(data.get('deadline', task.deadline.isoformat()))
    except ValueError:
        return jsonify({'message': 'Invalid datetime format. Use ISO 8601 format.'}), 400

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    
    db.session.commit()
    app.logger.info(f"Task {task.title} updated successfully")
    return jsonify({'message': 'Task updated successfully'}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    app.logger.info(f"Task {task.title} deleted successfully")
    return jsonify({'message': 'Task deleted successfully'}), 200

@app.route('/resources', methods=['POST'])
@jwt_required(optional=True)
def create_resource():
    data = request.get_json()
    new_resource = Resource(
        name=data['name'],
        type=data['type'],
        status=data['status'],
        event_id=data['event_id'],
        reserved_by=data.get('reserved_by', None)
    )
    db.session.add(new_resource)
    db.session.commit()
    app.logger.info(f"Resource {new_resource.name} created successfully")
    return jsonify({'message': 'Resource created successfully'}), 201

@app.route('/resources', methods=['GET'])
@jwt_required(optional=True)
def get_all_resources():
    resources = Resource.query.all()
    app.logger.info('Fetched all resources')
    return jsonify([
        {
            'id': resource.id,
            'name': resource.name,
            'type': resource.type,
            'status': resource.status,
            'event_id': resource.event_id,
            'reserved_by': resource.reserved_by
        }
        for resource in resources
    ]), 200

@app.route('/resources/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    app.logger.info(f'Resource {resource.name} fetched')
    return jsonify({
        'id': resource.id,
        'name': resource.name,
        'type': resource.type,
        'status': resource.status,
        'event_id': resource.event_id,
        'reserved_by': resource.reserved_by
    }), 200

@app.route('/resources/<int:resource_id>', methods=['PUT'])
@jwt_required(optional=True)
def update_resource(resource_id):
    data = request.get_json()
    resource = Resource.query.get_or_404(resource_id)
    resource.name = data.get('name', resource.name)
    resource.type = data.get('type', resource.type)
    resource.status = data.get('status', resource.status)
    resource.reserved_by = data.get('reserved_by', resource.reserved_by)
    db.session.commit()
    app.logger.info(f"Resource {resource.name} updated successfully")
    return jsonify({'message': 'Resource updated successfully'}), 200

@app.route('/resources/<int:resource_id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    db.session.delete(resource)
    db.session.commit()
    app.logger.info(f"Resource {resource.name} deleted successfully")
    return jsonify({'message': 'Resource deleted successfully'}), 200

@app.route('/expenses', methods=['POST'])
@jwt_required(optional=True)
def create_expense():
    data = request.get_json()
    new_expense = Expense(
        amount=data['amount'],
        description=data.get('description', ''),
        event_id=data['event_id']
    )
    db.session.add(new_expense)
    db.session.commit()
    app.logger.info(f"Expense recorded: {new_expense.amount}")
    return jsonify({'message': 'Expense recorded successfully'}), 201

@app.route('/expenses', methods=['GET'])
@jwt_required(optional=True)
def get_all_expenses():
    expenses = Expense.query.all()
    app.logger.info('Fetched all expenses')
    return jsonify([
        {
            'id': expense.id,
            'amount': expense.amount,
            'description': expense.description,
            'event_id': expense.event_id
        }
        for expense in expenses
    ]), 200

@app.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    app.logger.info(f'Expense {expense.amount} fetched')
    return jsonify({
        'id': expense.id,
        'amount': expense.amount,
        'description': expense.description,
        'event_id': expense.event_id
    }), 200

@app.route('/expenses/<int:expense_id>', methods=['PUT'])
@jwt_required(optional=True)
def update_expense(expense_id):
    data = request.get_json()
    expense = Expense.query.get_or_404(expense_id)
    expense.amount = data.get('amount', expense.amount)
    expense.description = data.get('description', expense.description)
    db.session.commit()
    app.logger.info(f"Expense {expense.amount} updated successfully")
    return jsonify({'message': 'Expense updated successfully'}), 200

@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    app.logger.info(f"Expense {expense.amount} deleted successfully")
    return jsonify({'message': 'Expense deleted successfully'}), 200

@app.route('/notifications', methods=['POST'])
@jwt_required(optional=True)
def create_notification():
    data = request.get_json()
    new_notification = Notification(
        title=data['title'],
        message=data['message'],
        user_id=get_jwt_identity(),
        created_at=datetime.utcnow()
    )
    db.session.add(new_notification)
    db.session.commit()
    app.logger.info(f"Notification {new_notification.title} created successfully")
    return jsonify({'message': 'Notification created successfully'}), 201

@app.route('/notifications', methods=['GET'])
@jwt_required(optional=True)
def get_notifications():
    notifications = Notification.query.filter_by(user_id=get_jwt_identity()).all()
    app.logger.info('Fetched all notifications')
    return jsonify([{
        'id': notification.id,
        'title': notification.title,
        'message': notification.message,
        'created_at': notification.created_at.isoformat()
    } for notification in notifications]), 200

@app.route('/notifications/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    app.logger.info(f'Notification {notification.title} fetched')
    return jsonify({
        'id': notification.id,
        'title': notification.title,
        'message': notification.message,
        'created_at': notification.created_at.isoformat()
    }), 200

@app.route('/notifications/<int:notification_id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    db.session.delete(notification)
    db.session.commit()
    app.logger.info(f"Notification {notification.title} deleted successfully")
    return jsonify({'message': 'Notification deleted successfully'}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5555))
    app.run(host="0.0.0.0", port=port, debug=True)
