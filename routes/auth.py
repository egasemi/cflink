from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)