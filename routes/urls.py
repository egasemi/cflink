from flask import Blueprint, request, jsonify
from services.url_service import create_short_url, edit_url, delete_url
from flask_jwt_extended import jwt_required

bp = Blueprint('urls', __name__, url_prefix='/api/urls')

@bp.route('/shorten', methods=['POST'])
@jwt_required()
def shorten():
    data = request.get_json()
    return create_short_url(data)

@bp.route('/edit/<int:url_id>', methods=['PUT'])
@jwt_required()
def edit(url_id):
    data = request.get_json()
    return edit_url(url_id, data)

@bp.route('/delete/<int:url_id>', methods=['DELETE'])
@jwt_required()
def delete(url_id):
    return delete_url(url_id)