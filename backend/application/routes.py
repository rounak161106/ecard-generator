from flask import current_app as app, jsonify, request, abort, send_from_directory
from application.models import User, UserCardDetail
from application.database import db
from flask_jwt_extended import create_access_token, jwt_required, current_user
from functools import wraps
import random, string, os
from celery.result import AsyncResult
from .tasks import csv_report, monthly_report, generate_msg, is_broker_available

# role required decorator
def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify(msg="Access denied: insufficient role"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route('/', methods=['GET'])
def index():
    return jsonify(message="Welcome to the Flask API!"), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "username and password are required."}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token, role=user.role, username=user.username), 200
    else:
        abort(401, description="Invalid username or password")

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "All fields are required."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists."}), 400

    user = User(username=username, email=email, password=password, role="user")
    db.session.add(user)
    db.session.commit()

    return jsonify(message="User registered successfully."), 201

@app.route("/api/dashboard", methods=['GET'])
@jwt_required()
def dashboard():
    if current_user.role == "admin":
        users = len(User.query.filter_by(role = "user").all())
        card_requests = UserCardDetail.query.filter_by(attr_name = "status").all()
        requested = under_verification = verified = generated = 0
        card_request_json = []
        for detail in card_requests:
            detail_dict = {}
            detail_dict["id"] = detail.id
            detail_dict["user_id"] = detail.user_id
            detail_dict["username"] = detail.bearer.username if detail.bearer else "Unknown"
            detail_dict["email"] = detail.bearer.email if detail.bearer else ""
            detail_dict["cardname"] = detail.cardname
            detail_dict["status"] = detail.attr_val
            if detail.attr_val == "requested":
                requested += 1
            elif detail.attr_val == "under_verification":
                under_verification += 1
            elif detail.attr_val == "verified":
                verified += 1
            elif detail.attr_val == "generated":
                generated += 1
            card_request_json.append(detail_dict)
        return jsonify({
            "role": current_user.role,
            "admin_name": current_user.username,
            "users": users,
            "card_requests": requested,
            "under_verification": under_verification,
            "verified": verified,
            "card_granted": generated,
            "available_cards": 4,
            "card_request_details": card_request_json
        })
    else:
        user_card_details = UserCardDetail.query.filter_by(attr_name = "status", user_id = current_user.id).all()
        available_cards = []
        card_requests = []
        for detail in user_card_details:
            detail_dict = {}
            detail_dict["cardname"] = detail.cardname
            detail_dict["status"] = detail.attr_val
            if detail.attr_val == "generated":
                key_detail = UserCardDetail.query.filter_by(user_id=current_user.id, cardname=detail.cardname, attr_name="key").first()
                detail_dict["key"] = key_detail.attr_val if key_detail else ""
                available_cards.append(detail_dict)
            else:
                card_requests.append(detail_dict)
        return jsonify({
            "role": current_user.role,
            "username": current_user.username,
            "available_cards": available_cards,
            "card_requests": card_requests
        })

@app.route('/api/request/<string:cardname>', methods=['POST'])
@role_required('user')
def request_card(cardname):
    # Check if a card of this type already exists for current user
    existing = UserCardDetail.query.filter_by(user_id=current_user.id, cardname=cardname, attr_name="status").first()
    if existing:
        return jsonify({"error": f"You already have a {cardname} card request with status: {existing.attr_val}"}), 400

    data = request.get_json() or {}

    if cardname == "aadhar":
        fullname = data.get("fullname", "")
        dob = data.get("dob", "")
        address = data.get("address", "")
        gender = data.get("gender", "")
        ph = data.get("ph", "")

        if not fullname or not dob or not address or not gender or not ph:
            return jsonify({"error": "All fields are required for Aadhaar card."}), 400

        attr1 = UserCardDetail(attr_name = "fullname", attr_val = fullname, cardname = cardname, user_id = current_user.id)
        attr2 = UserCardDetail(attr_name = "dob", attr_val = dob, cardname = cardname, user_id = current_user.id)
        attr3 = UserCardDetail(attr_name = "address", attr_val = address, cardname = cardname, user_id = current_user.id)
        attr4 = UserCardDetail(attr_name = "gender", attr_val = gender, cardname = cardname, user_id = current_user.id)
        attr5 = UserCardDetail(attr_name = "ph", attr_val = ph, cardname = cardname, user_id = current_user.id)
        attr6 = UserCardDetail(attr_name = "status", attr_val = "requested", cardname = cardname, user_id = current_user.id)

        db.session.add_all([attr1, attr2, attr3, attr4, attr5, attr6])
        db.session.commit()

    elif cardname == "pan":
        fullname = data.get("fullname", "")
        dob = data.get("dob", "")
        ph = data.get("ph", "")

        if not fullname or not dob or not ph:
            return jsonify({"error": "All fields are required for PAN card."}), 400

        attr1 = UserCardDetail(attr_name = "fullname", attr_val = fullname, cardname = cardname, user_id = current_user.id)
        attr2 = UserCardDetail(attr_name = "dob", attr_val = dob, cardname = cardname, user_id = current_user.id)
        attr3 = UserCardDetail(attr_name = "ph", attr_val = ph, cardname = cardname, user_id = current_user.id)
        attr4 = UserCardDetail(attr_name = "status", attr_val = "requested", cardname = cardname, user_id = current_user.id)

        db.session.add_all([attr1, attr2, attr3, attr4])
        db.session.commit()

    elif cardname in ["voter", "election"]:
        fullname = data.get("fullname", "")
        dob = data.get("dob", "")
        address = data.get("address", "")
        ward = data.get("ward", "")
        ph = data.get("ph", "")

        if not fullname or not dob or not address or not ward or not ph:
            return jsonify({"error": "All fields are required for Voter ID card."}), 400

        attr1 = UserCardDetail(attr_name = "fullname", attr_val = fullname, cardname = cardname, user_id = current_user.id)
        attr2 = UserCardDetail(attr_name = "dob", attr_val = dob, cardname = cardname, user_id = current_user.id)
        attr3 = UserCardDetail(attr_name = "address", attr_val = address, cardname = cardname, user_id = current_user.id)
        attr4 = UserCardDetail(attr_name = "ward", attr_val = ward, cardname = cardname, user_id = current_user.id)
        attr5 = UserCardDetail(attr_name = "ph", attr_val = ph, cardname = cardname, user_id = current_user.id)
        attr6 = UserCardDetail(attr_name = "status", attr_val = "requested", cardname = cardname, user_id = current_user.id)

        db.session.add_all([attr1, attr2, attr3, attr4, attr5, attr6])
        db.session.commit()

    else: # driving licence
        fullname = data.get("fullname", "")
        v_no = data.get("v_no", "")
        v_type = data.get("type", "")

        if not fullname or not v_no or not v_type:
            return jsonify({"error": "All fields are required for Driving Licence."}), 400

        attr1 = UserCardDetail(attr_name = "fullname", attr_val = fullname, cardname = cardname, user_id = current_user.id)
        attr2 = UserCardDetail(attr_name = "v_no", attr_val = v_no, cardname = cardname, user_id = current_user.id)
        attr3 = UserCardDetail(attr_name = "type", attr_val = v_type, cardname = cardname, user_id = current_user.id)
        attr4 = UserCardDetail(attr_name = "status", attr_val = "requested", cardname = cardname, user_id = current_user.id)

        db.session.add_all([attr1, attr2, attr3, attr4])
        db.session.commit()

    return jsonify(message = f"request for {cardname} made successfully"), 201

@app.route("/api/generate/<string:cardname>/<int:user_id>", methods=['GET', 'POST'])
@role_required("admin")
def generate(cardname, user_id):
    # status to change to "generated"
    detail = UserCardDetail.query.filter_by(user_id=user_id, cardname=cardname, attr_name="status").first()
    if not detail:
        return jsonify({"error": f"Card request for {cardname} not found for user {user_id}"}), 404

    detail.attr_val = "generated"
    db.session.commit()

    # creating unique key wrt card
    key = ""
    if cardname == "aadhar":
        key = str(random.randint(10**11, 10**12 - 1)) # 12 digit number
    elif cardname == "pan":
        first_part = ''.join(random.choices(string.ascii_uppercase, k=5))
        middle_part = ''.join(random.choices(string.digits, k=4))
        last_part = random.choice(string.ascii_uppercase)
        key = first_part + middle_part + last_part # ABCDE1234F
    elif cardname in ["driving", "driving_licence"]:
        part1 = ''.join(random.choices(string.ascii_uppercase, k=2))
        part2 = ''.join(random.choices(string.digits, k=2))
        part3 = ''.join(random.choices(string.digits, k=7))
        key = part1 + "-" + part2 + "-2025-" + part3 # AB-12-2025-3456789
    elif cardname in ["voter", "election"]:
        first_part = ''.join(random.choices(string.ascii_uppercase, k=3))
        last_part = ''.join(random.choices(string.digits, k=7))
        key = first_part + last_part # ABC1234567
    else:
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    existing_key = UserCardDetail.query.filter_by(user_id=user_id, cardname=cardname, attr_name="key").first()
    if existing_key:
        existing_key.attr_val = str(key)
    else:
        info1 = UserCardDetail(attr_name="key", attr_val=str(key), cardname=cardname, user_id=user_id)
        db.session.add(info1)
    db.session.commit()

    if is_broker_available():
        try:
            generate_msg.apply_async((detail.bearer.username, cardname), retry=False)
        except Exception as e:
            print("[Celery generate_msg notice]", e)
    else:
        print(f"[Celery notice] Broker offline. Skipping async webhook notice for {cardname}.")

    return jsonify({
        "message": f"{cardname} card created for user: {user_id}",
        "key": str(key)
    }), 200

# Update card status api route 
@app.route("/api/update/<string:cardname>/<int:user_id>", methods=['POST', 'PUT'])
@role_required("admin")
def update_status(cardname, user_id):
    data = request.get_json() or {}
    new_status = data.get("status", None)
    if not new_status:
        return jsonify({"error": "Status is required"}), 400

    detail = UserCardDetail.query.filter_by(user_id=user_id, cardname=cardname, attr_name="status").first()
    if not detail:
        return jsonify({"error": "Card request not found"}), 404

    old_status = detail.attr_val
    detail.attr_val = new_status
    db.session.commit()
    return jsonify(message = f"card status changed from {old_status} to {new_status}.")

# View card api route 
@app.route("/api/view/<string:cardname>", methods=['GET'])
@role_required("user")
def view_card(cardname):
    card_details = UserCardDetail.query.filter_by(user_id=current_user.id, cardname=cardname).all()
    if not card_details:
        return jsonify({"error": f"No {cardname} card found for current user"}), 404

    details_json = []
    details_map = {}
    for detail in card_details:
        detail_dict = {
            "attr_name": detail.attr_name,
            "attr_val": detail.attr_val
        }
        details_json.append(detail_dict)
        details_map[detail.attr_name] = detail.attr_val

    return jsonify({
        "cardname": cardname,
        "username": current_user.username,
        "email": current_user.email,
        "status": details_map.get("status", "unknown"),
        "key": details_map.get("key", ""),
        "details": details_json,
        "data": details_map
    }), 200

# Delete card (User deletes own card / cancels request)
@app.route("/api/delete/<string:cardname>", methods=['POST', 'DELETE'])
@role_required("user")
def delete_user_card(cardname):
    details = UserCardDetail.query.filter_by(user_id=current_user.id, cardname=cardname).all()
    if not details:
        return jsonify({"error": f"No {cardname} card found to delete"}), 404

    for d in details:
        db.session.delete(d)
    db.session.commit()
    return jsonify(message = f"{cardname} card deleted successfully."), 200

# Delete card (Admin deletes any user's card)
@app.route("/api/delete/<string:cardname>/<int:user_id>", methods=['POST', 'DELETE'])
@role_required("admin")
def delete_admin_card(cardname, user_id):
    details = UserCardDetail.query.filter_by(user_id=user_id, cardname=cardname).all()
    if not details:
        return jsonify({"error": f"No {cardname} card found for user {user_id}"}), 404

    for d in details:
        db.session.delete(d)
    db.session.commit()
    return jsonify(message = f"{cardname} card for user {user_id} deleted successfully."), 200

# User Profile routes
@app.route("/api/user/profile", methods=['GET'])
@jwt_required()
def get_user_profile():
    status_records = UserCardDetail.query.filter_by(user_id=current_user.id, attr_name="status").all()
    total_cards = len(status_records)
    generated_cards = len([s for s in status_records if s.attr_val == "generated"])
    pending_cards = total_cards - generated_cards

    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "total_cards": total_cards,
        "generated_cards": generated_cards,
        "pending_cards": pending_cards
    }), 200

@app.route("/api/user/update", methods=['POST', 'PUT'])
@jwt_required()
def update_user_profile():
    data = request.get_json() or {}
    new_email = data.get("email")
    new_password = data.get("password")

    if new_email:
        existing = User.query.filter_by(email=new_email).first()
        if existing and existing.id != current_user.id:
            return jsonify({"error": "Email is already taken by another account."}), 400
        current_user.email = new_email

    if new_password:
        if len(new_password) < 4:
            return jsonify({"error": "Password must be at least 4 characters."}), 400
        current_user.password = new_password

    db.session.commit()
    return jsonify(message = "Profile updated successfully.", email = current_user.email), 200

# Backend jobs trigger
@app.route('/export_csv', methods=['GET'])
@jwt_required()
def export():
    if is_broker_available():
        try:
            result = csv_report.apply_async(retry=False)
            return jsonify({
                "id": result.id,
                "status": "Task scheduled via Celery"
            }), 202
        except Exception as e:
            print("[Celery export error]", e)

    # Fallback to direct synchronous execution if Celery broker is offline
    filename = csv_report()
    return jsonify({
        "id": "direct_run",
        "filename": filename,
        "status": "Generated directly (Celery broker offline)"
    }), 200

@app.route('/api/csv_status/<id>', methods=['GET'])
def csv_status(id):
    if id == "direct_run":
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        files = sorted(os.listdir(static_dir), reverse=True) if os.path.exists(static_dir) else []
        latest = files[0] if files else None
        return jsonify({
            "id": id,
            "state": "SUCCESS",
            "ready": True,
            "successful": True,
            "filename": latest
        }), 200

    try:
        res = AsyncResult(id)
        is_ready = res.ready()
        is_success = res.successful() if is_ready else False
        return jsonify({
            "id": id,
            "state": res.state, # PENDING, STARTED, SUCCESS, FAILURE
            "ready": is_ready,
            "successful": is_success,
            "filename": res.result if (is_ready and is_success) else None
        }), 200
    except Exception as e:
        return jsonify({
            "id": id,
            "state": "FAILURE",
            "ready": True,
            "successful": False,
            "error": str(e)
        }), 200

@app.route('/api/csv_result/<id>', methods=['GET'])
def csv_result(id):
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    if id == "direct_run":
        files = sorted(os.listdir(static_dir), reverse=True) if os.path.exists(static_dir) else []
        if files:
            return send_from_directory(static_dir, files[0], as_attachment=True)
        return jsonify({"error": "No CSV files found"}), 404

    try:
        res = AsyncResult(id)
        if not res.ready() or not res.successful():
            return jsonify({"error": "CSV file not ready yet"}), 400
        return send_from_directory(static_dir, res.result, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
