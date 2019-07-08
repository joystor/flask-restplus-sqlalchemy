from authlib.flask.oauth2 import (
    AuthorizationServer,
    ResourceProtector
)
from authlib.flask.oauth2.sqla import (
    create_save_token_func,
    create_revocation_endpoint,
    create_bearer_token_validator,
)
from authlib.oauth2.rfc6749.grants import (
    AuthorizationCodeGrant as _AuthorizationCodeGrant,
    ImplicitGrant as _ImplicitGrant,
    ResourceOwnerPasswordCredentialsGrant as _ResourceOwnerPasswordCredentialsGrant,
    ClientCredentialsGrant as _ClientCredentialsGrant,
    RefreshTokenGrant as _RefreshTokenGrant,
)
from werkzeug.security import gen_salt
from flask import request
from flask import session as SessionApp
from api.database import db
from api.database.models import (
    User, UserInfo, 
    VwOAuth2ClientUsers, OAuth2Token
)

from flask import current_app

class PasswordGrant(_ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, username, password):
        current_app.logger.info('PasswordGrant.authenticate_user')
        user = User.query.filter_by(username=username).first()
        if user.check_password(password):
            return user


class RefreshTokenGrant(_RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):
        current_app.logger.info('RefreshTokenGrant.authenticate_refresh_token')
        token  = OAuth2Token.query.filter_by(refresh_token=refresh_token).first()
        if token and not token.revoked and not token.is_refresh_token_expired():
            return token

    def authenticate_user(self, credential):
        current_app.logger.info('RefreshTokenGrant.authenticate_user')
        return User.query.get(credential.user_id)
    
    
def create_query_client_func(session, client_model):
    def query_client(client_id):
        id = -1
        if 'id' in SessionApp:
            id = SessionApp['id']
        q = session.query(client_model)
        return q.filter_by(client_id=client_id, user_id=id).first()
    return query_client

query_client = create_query_client_func(db.session, VwOAuth2ClientUsers)
save_token = create_save_token_func(db.session, OAuth2Token)
authorization = AuthorizationServer(
    query_client=query_client,
    save_token=save_token,
)
require_oauth = ResourceProtector()


def config_oauth(app):
    app.logger.info("Configuring oAuth2.0")
    authorization.init_app(app)
    #Grant password
    authorization.register_grant(PasswordGrant)
    authorization.register_grant(RefreshTokenGrant)
    
    # support revocation
    revocation_cls = create_revocation_endpoint(db.session, OAuth2Token)
    authorization.register_endpoint(revocation_cls)

    # protect resource
    bearer_cls = create_bearer_token_validator(db.session, OAuth2Token)
    require_oauth.register_token_validator(bearer_cls())