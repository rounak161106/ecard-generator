from flask import current_app as app, jsonify, request, abort
from application.models import User, UserCardDetail
from application.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/', methods=['GET'])
def index():
    return jsonify(message="Welcome to the Flask API!"), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "username and password are required."}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token), 200
    else:
        abort(401, description="Invalid username or password")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)
    username = data.get('username')
    print(username)
    email = data.get('email')
    password = data.get('password')
    print(username, email, password, sep=' | ')

    if not username or not email or not password:
        return jsonify({"error": "All fields are required."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists."}), 400

    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify(message="User registered successfully."), 201