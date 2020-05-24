from app.api import bp
from flask import jsonify, request, url_for
from app import db
from app.models import User, Credential
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/credentials/<int:id>', methods=['POST'])
@token_auth.login_required
def create_credential(id):
    user = User.query.get_or_404(id)
    if not user:
        return bad_request('please use a different user ID')
    data = request.get_json() or {}
    if 'username' not in data or 'comments' not in data or 'password' not in data:
        return bad_request('must include username, comments and password fields')
    if user and Credential.query.filter_by(comments=data['comments']).first():
        return bad_request('please use a comment')
    credential = Credential()
    credential.from_dict(data, new_credential=True)
    credential.owner = user
    db.session.add(credential)
    db.session.commit()
    response = jsonify(credential.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response
