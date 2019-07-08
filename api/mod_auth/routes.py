from flask import Blueprint, request, session, current_app
from flask import render_template, redirect, jsonify
from urllib.parse import urlencode
from werkzeug.security import gen_salt
from authlib.flask.oauth2 import current_token
from authlib.oauth2 import OAuth2Error, OAuth2Request
from authlib.oauth2.rfc6749 import InvalidRequestError
from authlib.common.encoding import to_unicode
from api.database import db
from api.database.models import User, UserInfo, VwOAuth2ClientUsers, OAuth2Client, OAuth2Token
from api.mod_auth.oauth2 import authorization, require_oauth

bp_oauth2 = Blueprint('oauth2', __name__)

def current_user():
    if 'id' in session:
        current_app.logger.info('User in session')
        uid = session['id']
        return User.query.filter_by(id_user=uid).first()
    else:
        user = None
        username = request.form.get('username')
        if username:
            current_app.logger.info('Getting User in parameters')
            user = User.query.filter_by(username=username).first()
            if user:
                current_app.logger.info('User id:{0}'.format(user.id_user))
                session['id'] = user.id_user
        return user
    return None


@bp_oauth2.route('/oauth/login', methods=['POST'])
def login():
    user = current_user()
    if user:
        if user.check_password(request.form.get('password')):
            q = VwOAuth2ClientUsers.query.filter_by(client_id=request.form.get('client_id'), user_id=user.id_user).first()
            return jsonify(client_secret=q.client_secret)
        else:
            return jsonify(error="password not match")
    else:
        return jsonify(error="user/password not found")


@bp_oauth2.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')

@bp_oauth2.route('/oauth/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()

@bp_oauth2.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')

@bp_oauth2.route('/api/me', methods=['GET','POST'])
@require_oauth()
def api_me():
    user = current_token.user
    if user:
        return jsonify(id=user.id_user, username=user.username)
    else:
        return jsonify(error="Not user")

@bp_oauth2.route('/api/me_ses', methods=['GET','POST'])
def me_ses():
    user = current_user()
    if user:
        return jsonify(id=user.id_user, username=user.username)
    else:
        return jsonify(error="Not user")

