from flask import current_app as app, jsonify, request, abort
from application.models import User, UserCardDetail
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity