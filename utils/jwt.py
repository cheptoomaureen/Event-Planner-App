
# from flask import Flask, request, jsonify
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from werkzeug.security import generate_password_hash, check_password_hash
# from flasgger import Swagger, swag_from
# from flask_swagger_ui import get_swaggerui_blueprint
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from datetime import datetime
# import os
# import logging
# import secrets
# from flask.json.provider import DefaultJSONProvider
# JSONEncoder = DefaultJSONProvider

# # Initialize the Flask application
# app = Flask(__name__)

# # Configuration
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(16))
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///database.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_hex(16))
# app.config['SWAGGER'] = {
#     'title': 'Event Planner App API',
#     'uiversion': 3,
#     'description': 'API documentation for the Event Planner App',
#     'version': '1.0.0'
# }
# app.config['DEBUG'] = os.getenv('FLASK_DEBUG', True)  # Set to False in production

# # Initialize extensions
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# jwt = JWTManager(app)
# swagger = Swagger(app)

# # Logging setup
# logging.basicConfig(level=logging.DEBUG)

# # Import models after db initialization
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     events = db.relationship('Event', backref='creator', lazy=True)
#     notifications = db.relationship('Notification', backref='user', lazy=True)

#     def __repr__(self):
#         return f'<User {self.username}>'

# class Event(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     date = db.Column(db.DateTime, nullable=False)
#     location = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     tasks = db.relationship('Task', backref='event', lazy=True)
#     resources = db.relationship('Resource', backref='event', lazy=True)
#     expenses = db.relationship('Expense', backref='event', lazy=True)

#     def __repr__(self):
#         return f'<Event {self.title}>'

# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     deadline = db.Column(db.DateTime, nullable=False)
#     priority = db.Column(db.String(50), nullable=False)
#     status = db.Column(db.String(50), nullable=False, default='Pending')
#     event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
#     assigned_to = db.Column(db.String(80), nullable=False)

#     def __repr__(self):
#         return f'<Task {self.title}>'

# class Resource(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     type = db.Column(db.String(100), nullable=False)
#     status = db.Column(db.String(50), nullable=False)
#     event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
#     reserved_by = db.Column(db.String(80), nullable=True)

#     def __repr__(self):
#         return f'<Resource {self.name}>'

# class Expense(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     amount = db.Column(db.Float, nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

#     def __repr__(self):
#         return f'<Expense {self.amount}>'

# class Notification(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     message = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return f'<Notification {self.title}>'

# # Create database tables if they don't exist (useful for initial development)
# with app.app_context():
#     db.create_all()

# # Define routes and handlers
# @app.route('/')
# def index():
#     return "Welcome to the Event Planner App API!"

# @app.route('/auth/register', methods=['POST'])
# @swag_from({
#     'summary': 'Register a new user',
#     'description': 'This endpoint registers a new user with a username, email, and password.',
#     'consumes': ['application/json'],
#     'produces': ['application/json'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'username': {'type': 'string'},
#                     'email': {'type': 'string'},
#                     'password': {'type': 'string'}
#                 },
#                 'required': ['username', 'email', 'password']
#             }
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'User registered successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def register():
#     from models import User  # Inline import to avoid circular dependency
#     data = request.get_json()
#     hashed_password = generate_password_hash(data['password'], method='sha256')
#     new_user = User(username=data['username'], email=data['email'], password=hashed_password)
#     db.session.add(new_user)
#     db.session.commit()
#     logging.info(f"User registered: {new_user.username}")
#     return jsonify({'message': 'User registered successfully'})

# @app.route('/auth/login', methods=['POST'])
# @swag_from({
#     'summary': 'User login',
#     'description': 'This endpoint allows a user to login with an email and password.',
#     'consumes': ['application/json'],
#     'produces': ['application/json'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'email': {'type': 'string'},
#                     'password': {'type': 'string'}
#                 },
#                 'required': ['email', 'password']
#             }
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'User logged in successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'token': {'type': 'string'}
#                 }
#             }
#         },
#         401: {
#             'description': 'Invalid credentials',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })

# @app.route('/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     user = User.query.filter_by(email=data['email']).first()
#     if user and check_password_hash(user.password, data['password']):
#         token = create_access_token(identity=user.id)
#         logging.info(f"User logged in: {user.username}")
#         return jsonify({'token': token})
#     return jsonify({'message': 'Invalid credentials'}), 401


# @app.route('/events', methods=['POST'])
# @jwt_required()
# @swag_from({
#     'summary': 'Create a new event',
#     'description': 'This endpoint allows a user to create a new event.',
#     'consumes': ['application/json'],
#     'produces': ['application/json'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'title': {'type': 'string'},
#                     'date': {'type': 'string', 'format': 'date-time'},
#                     'location': {'type': 'string'},
#                     'description': {'type': 'string'}
#                 },
#                 'required': ['title', 'date', 'location']
#             }
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'Event created successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def create_event():
#     from models import Event  # Inline import to avoid circular dependency
#     data = request.get_json()
#     user_id = get_jwt_identity()
#     new_event = Event(
#         title=data['title'],
#         date=datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S'),
#         location=data['location'],
#         description=data.get('description', ''),
#         created_by=user_id
#     )
#     db.session.add(new_event)
#     db.session.commit()
#     logging.info(f"Event created: {new_event.title} by user {user_id}")
#     return jsonify({'message': 'Event created successfully'})

# @app.route('/events', methods=['GET'])
# @jwt_required()
# @swag_from({
#     'summary': 'Get list of events',
#     'description': 'This endpoint returns a list of events created by the authenticated user.',
#     'produces': ['application/json'],
#     'responses': {
#         200: {
#             'description': 'List of events',
#             'schema': {
#                 'type': 'array',
#                 'items': {
#                     'type': 'object',
#                     'properties': {
#                         'id': {'type': 'integer'},
#                         'title': {'type': 'string'},
#                         'date': {'type': 'string', 'format': 'date-time'},
#                         'location': {'type': 'string'},
#                         'description': {'type': 'string'}
#                     }
#                 }
#             }
#         }
#     }
# })
# def get_events():
#     from models import Event  # Inline import to avoid circular dependency
#     user_id = get_jwt_identity()
#     events = Event.query.filter_by(created_by=user_id).all()
#     return jsonify([{
#         'id': event.id,
#         'title': event.title,
#         'date': event.date.isoformat(),
#         'location': event.location,
#         'description': event.description
#     } for event in events])

# @app.route('/events/<int:event_id>', methods=['PUT'])
# @jwt_required()
# @swag_from({
#     'summary': 'Update an event',
#     'description': 'This endpoint updates an existing event.',
#     'consumes': ['application/json'],
#     'produces': ['application/json'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'title': {'type': 'string'},
#                     'date': {'type': 'string', 'format': 'date-time'},
#                     'location': {'type': 'string'},
#                     'description': {'type': 'string'}
#                 },
#                 'required': ['title', 'date', 'location']
#             }
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'Event updated successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         },
#         404: {
#             'description': 'Event not found',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def update_event(event_id):
#     from models import Event  # Inline import to avoid circular dependency
#     data = request.get_json()
#     event = Event.query.get(event_id)
#     if not event:
#         return jsonify({'message': 'Event not found'}), 404

#     event.title = data['title']
#     event.date = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S')
#     event.location = data['location']
#     event.description = data.get('description', event.description)
#     db.session.commit()
#     logging.info(f"Event updated: {event.title} by user {get_jwt_identity()}")
#     return jsonify({'message': 'Event updated successfully'})

# @app.route('/events/<int:event_id>', methods=['DELETE'])
# @jwt_required()
# @swag_from({
#     'summary': 'Delete an event',
#     'description': 'This endpoint deletes an existing event.',
#     'produces': ['application/json'],
#     'responses': {
#         200: {
#             'description': 'Event deleted successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         },
#         404: {
#             'description': 'Event not found',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def delete_event(event_id):
#     from models import Event  # Inline import to avoid circular dependency
#     event = Event.query.get(event_id)
#     if not event:
#         return jsonify({'message': 'Event not found'}), 404

#     db.session.delete(event)
#     db.session.commit()
#     logging.info(f"Event deleted: {event.title} by user {get_jwt_identity()}")
#     return jsonify({'message': 'Event deleted successfully'})

# @app.route('/tasks', methods=['POST'])
# @jwt_required()
# @swag_from({
#     'summary': 'Create a new task',
#     'description': 'This endpoint allows a user to create a new task for an event.',
#     'consumes': ['application/json'],
#     'produces': ['application/json'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'title': {'type': 'string'},
#                     'description': {'type': 'string'},
#                     'deadline': {'type': 'string', 'format': 'date-time'},
#                     'priority': {'type': 'string'},
#                     'status': {'type': 'string'},
#                     'event_id': {'type': 'integer'},
#                     'assigned_to': {'type': 'string'}
#                 },
#                 'required': ['title', 'deadline', 'priority', 'event_id', 'assigned_to']
#             }
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'Task created successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def create_task():
#     from models import Task  # Inline import to avoid circular dependency
#     data = request.get_json()
#     new_task = Task(
#         title=data['title'],
#         description=data.get('description', ''),
#         deadline=datetime.strptime(data['deadline'], '%Y-%m-%dT%H:%M:%S'),
#         priority=data['priority'],
#         status=data.get('status', 'Pending'),
#         event_id=data['event_id'],
#         assigned_to=data['assigned_to']
#     )
#     db.session.add(new_task)
#     db.session.commit()
#     logging.info(f"Task created: {new_task.title}")
#     return jsonify({'message': 'Task created successfully'})

# @app.route('/tasks/<int:task_id>', methods=['PUT'])
# @jwt_required()
# @swag_from({
#     'summary': 'Update a task',
#     'description': 'This endpoint updates an existing task.',
#     'consumes': ['application/json'],
#     'produces': ['application/json'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'title': {'type': 'string'},
#                     'description': {'type': 'string'},
#                     'deadline': {'type': 'string', 'format': 'date-time'},
#                     'priority': {'type': 'string'},
#                     'status': {'type': 'string'}
#                 },
#                 'required': ['title', 'deadline', 'priority']
#             }
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'Task updated successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         },
#         404: {
#             'description': 'Task not found',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def update_task(task_id):
#     from models import Task  # Inline import to avoid circular dependency
#     data = request.get_json()
#     task = Task.query.get(task_id)
#     if not task:
#         return jsonify({'message': 'Task not found'}), 404

#     task.title = data['title']
#     task.description = data.get('description', task.description)
#     task.deadline = datetime.strptime(data['deadline'], '%Y-%m-%dT%H:%M:%S')
#     task.priority = data['priority']
#     task.status = data.get('status', task.status)
#     db.session.commit()
#     logging.info(f"Task updated: {task.title}")
#     return jsonify({'message': 'Task updated successfully'})

# @app.route('/tasks/<int:task_id>', methods=['DELETE'])
# @jwt_required()
# @swag_from({
#     'summary': 'Delete a task',
#     'description': 'This endpoint deletes an existing task.',
#     'produces': ['application/json'],
#     'responses': {
#         200: {
#             'description': 'Task deleted successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         },
#         404: {
#             'description': 'Task not found',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def delete_task(task_id):
#     from models import Task  # Inline import to avoid circular dependency
#     task = Task.query.get(task_id)
#     if not task:
#         return jsonify({'message': 'Task not found'}), 404

#     db.session.delete(task)
#     db.session.commit()
#     logging.info(f"Task deleted: {task.title}")
#     return jsonify({'message': 'Task deleted successfully'})

# @app.route('/resources', methods=['POST'])
# @jwt_required()
# @swag_from({
#     'summary': 'Create a new resource',
#     'description': 'This endpoint allows a user to create a new resource for an event.',
#     'consumes': ['application/json'],
#     'produces': ['application/json'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'name': {'type': 'string'},
#                     'type': {'type': 'string'},
#                     'status': {'type': 'string'},
#                     'event_id': {'type': 'integer'},
#                     'reserved_by': {'type': 'string'}
#                 },
#                 'required': ['name', 'type', 'status', 'event_id']
#             }
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'Resource created successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def create_resource():
#     from models import Resource  # Inline import to avoid circular dependency
#     data = request.get_json()
#     new_resource = Resource(
#         name=data['name'],
#         type=data['type'],
#         status=data['status'],
#         event_id=data['event_id'],
#         reserved_by=data.get('reserved_by', None)
#     )
#     db.session.add(new_resource)
#     db.session.commit()
#     logging.info(f"Resource created: {new_resource.name}")
#     return jsonify({'message': 'Resource created successfully'})

# @app.route('/resources/<int:resource_id>', methods=['PUT'])
# @jwt_required()
# @swag_from({
#     'summary': 'Update a resource',
#     'description': 'This endpoint updates an existing resource.',
#     'consumes': ['application/json'],
#     'produces': ['application/json'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'name': {'type': 'string'},
#                     'type': {'type': 'string'},
#                     'status': {'type': 'string'},
#                     'reserved_by': {'type': 'string'}
#                 },
#                 'required': ['name', 'type', 'status']
#             }
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'Resource updated successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         },
#         404: {
#             'description': 'Resource not found',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def update_resource(resource_id):
#     from models import Resource  # Inline import to avoid circular dependency
#     data = request.get_json()
#     resource = Resource.query.get(resource_id)
#     if not resource:
#         return jsonify({'message': 'Resource not found'}), 404

#     resource.name = data['name']
#     resource.type = data['type']
#     resource.status = data['status']
#     resource.reserved_by = data.get('reserved_by', resource.reserved_by)
#     db.session.commit()
#     logging.info(f"Resource updated: {resource.name}")
#     return jsonify({'message': 'Resource updated successfully'})

# @app.route('/resources/<int:resource_id>', methods=['DELETE'])
# @jwt_required()
# @swag_from({
#     'summary': 'Delete a resource',
#     'description': 'This endpoint deletes an existing resource.',
#     'produces': ['application/json'],
#     'responses': {
#         200: {
#             'description': 'Resource deleted successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         },
#         404: {
#             'description': 'Resource not found',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def delete_resource(resource_id):
#     from models import Resource  # Inline import to avoid circular dependency
#     resource = Resource.query.get(resource_id)
#     if not resource:
#         return jsonify({'message': 'Resource not found'}), 404

#     db.session.delete(resource)
#     db.session.commit()
#     logging.info(f"Resource deleted: {resource.name}")
#     return jsonify({'message': 'Resource deleted successfully'})

# @app.route('/expenses', methods=['POST'])
# @jwt_required()
# @swag_from({
#     'summary': 'Record a new expense',
#     'description': 'This endpoint allows a user to record a new expense for an event.',
#     'consumes': ['application/json'],
#     'produces': ['application/json'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'amount': {'type': 'number'},
#                     'description': {'type': 'string'},
#                     'event_id': {'type': 'integer'}
#                 },
#                 'required': ['amount', 'event_id']
#             }
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'Expense recorded successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def create_expense():
#     from models import Expense  # Inline import to avoid circular dependency
#     data = request.get_json()
#     new_expense = Expense(
#         amount=data['amount'],
#         description=data.get('description', ''),
#         event_id=data['event_id']
#     )
#     db.session.add(new_expense)
#     db.session.commit()
#     logging.info(f"Expense recorded: {new_expense.amount}")
#     return jsonify({'message': 'Expense recorded successfully'})

# @app.route('/expenses/<int:expense_id>', methods=['PUT'])
# @jwt_required()
# @swag_from({
#     'summary': 'Update an expense',
#     'description': 'This endpoint updates an existing expense.',
#     'consumes': ['application/json'],
#     'produces': ['application/json'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'amount': {'type': 'number'},
#                     'description': {'type': 'string'}
#                 },
#                 'required': ['amount']
#             }
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'Expense updated successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         },
#         404: {
#             'description': 'Expense not found',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def update_expense(expense_id):
#     from models import Expense  # Inline import to avoid circular dependency
#     data = request.get_json()
#     expense = Expense.query.get(expense_id)
#     if not expense:
#         return jsonify({'message': 'Expense not found'}), 404

#     expense.amount = data['amount']
#     expense.description = data.get('description', expense.description)
#     db.session.commit()
#     logging.info(f"Expense updated: {expense.amount}")
#     return jsonify({'message': 'Expense updated successfully'})

# @app.route('/expenses/<int:expense_id>', methods=['DELETE'])
# @jwt_required()
# @swag_from({
#     'summary': 'Delete an expense',
#     'description': 'This endpoint deletes an existing expense.',
#     'produces': ['application/json'],
#     'responses': {
#         200: {
#             'description': 'Expense deleted successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         },
#         404: {
#             'description': 'Expense not found',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def delete_expense(expense_id):
#     from models import Expense  # Inline import to avoid circular dependency
#     expense = Expense.query.get(expense_id)
#     if not expense:
#         return jsonify({'message': 'Expense not found'}), 404

#     db.session.delete(expense)
#     db.session.commit()
#     logging.info(f"Expense deleted: {expense.amount}")
#     return jsonify({'message': 'Expense deleted successfully'})

# @app.route('/notifications', methods=['POST'])
# @jwt_required()
# @swag_from({
#     'summary': 'Create a new notification',
#     'description': 'This endpoint allows a user to create a new notification.',
#     'consumes': ['application/json'],
#     'produces': ['application/json'],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'title': {'type': 'string'},
#                     'message': {'type': 'string'}
#                 },
#                 'required': ['title', 'message']
#             }
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'Notification created successfully',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {'type': 'string'}
#                 }
#             }
#         }
#     }
# })
# def create_notification():
#     from models import Notification  # Inline import to avoid circular dependency
#     data = request.get_json()
#     new_notification = Notification(
#         title=data['title'],
#         message=data['message'],
#         user_id=get_jwt_identity(),
#         created_at=datetime.utcnow()
#     )
#     db.session.add(new_notification)
#     db.session.commit()
#     logging.info(f"Notification created: {new_notification.title} for user {new_notification.user_id}")
#     return jsonify({'message': 'Notification created successfully'})

# @app.route('/notifications', methods=['GET'])
# @jwt_required()
# @swag_from({
#     'summary': 'Get list of notifications',
#     'description': 'This endpoint returns a list of notifications for the authenticated user.',
#     'produces': ['application/json'],
#     'responses': {
#         200: {
#             'description': 'List of notifications',
#             'schema': {
#                 'type': 'array',
#                 'items': {
#                     'type': 'object',
#                     'properties': {
#                         'id': {'type': 'integer'},
#                         'title': {'type': 'string'},
#                         'message': {'type': 'string'},
#                         'created_at': {'type': 'string', 'format': 'date-time'}
#                     }
#                 }
#             }
#         }
#     }
# })
# def get_notifications():
#     from models import Notification  # Inline import to avoid circular dependency
#     notifications = Notification.query.filter_by(user_id=get_jwt_identity()).all()
#     return jsonify([{
#         'id': notification.id,
#         'title': notification.title,
#         'message': notification.message,
#         'created_at': notification.created_at.isoformat()
#     } for notification in notifications])

# # Swagger UI setup
# SWAGGER_URL = '/swagger'
# API_URL = '/static/swagger.yaml'  # Ensure this path is correct or exists
# swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Event Planner App API"})
# app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     print(f"Server is running at http://0.0.0.0:{port}")
#     app.run(host="0.0.0.0", port=port)
# #