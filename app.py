from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Import models
from models import User, Event, Task, Resource, Expense

# Routes
@app.route('/')
def index():
    return "Welcome to the Event Planner App API!"


@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_event = Event(
        title=data['title'],
        date=datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S'),
        location=data['location'],
        description=data.get('description', ''),
        created_by=user_id
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully'})

@app.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    user_id = get_jwt_identity()
    events = Event.query.filter_by(created_by=user_id).all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'date': event.date.isoformat(),
        'location': event.location,
        'description': event.description
    } for event in events])

@app.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    data = request.get_json()
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    
    event.title = data['title']
    event.date = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S')
    event.location = data['location']
    event.description = data.get('description', event.description)
    db.session.commit()
    return jsonify({'message': 'Event updated successfully'})

@app.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'})

@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        deadline=datetime.strptime(data['deadline'], '%Y-%m-%dT%H:%M:%S'),
        priority=data['priority'],
        status=data.get('status', 'Pending'),
        event_id=data['event_id'],
        assigned_to=data['assigned_to']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    task.title = data['title']
    task.description = data.get('description', task.description)
    task.deadline = datetime.strptime(data['deadline'], '%Y-%m-%dT%H:%M:%S')
    task.priority = data['priority']
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/resources', methods=['POST'])
@jwt_required()
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
    return jsonify({'message': 'Resource created successfully'})

@app.route('/resources/<int:resource_id>', methods=['PUT'])
@jwt_required()
def update_resource(resource_id):
    data = request.get_json()
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({'message': 'Resource not found'}), 404

    resource.name = data['name']
    resource.type = data['type']
    resource.status = data['status']
    resource.reserved_by = data.get('reserved_by', resource.reserved_by)
    db.session.commit()
    return jsonify({'message': 'Resource updated successfully'})

@app.route('/resources/<int:resource_id>', methods=['DELETE'])
@jwt_required()
def delete_resource(resource_id):
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({'message': 'Resource not found'}), 404

    db.session.delete(resource)
    db.session.commit()
    return jsonify({'message': 'Resource deleted successfully'})

@app.route('/expenses', methods=['POST'])
@jwt_required()
def create_expense():
    data = request.get_json()
    new_expense = Expense(
        amount=data['amount'],
        description=data.get('description', ''),
        event_id=data['event_id']
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'message': 'Expense recorded successfully'})

@app.route('/expenses/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    data = request.get_json()
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({'message': 'Expense not found'}), 404

    expense.amount = data['amount']
    expense.description = data.get('description', expense.description)
    db.session.commit()
    return jsonify({'message': 'Expense updated successfully'})

@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({'message': 'Expense not found'}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted successfully'})

if __name__ == "__main__":
    app.run(port=5555, debug=True)