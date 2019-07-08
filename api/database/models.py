import time
from api.database import db
from authlib.flask.oauth2.sqla import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base


class Base(db.Model):
    __abstract__  = True
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())
    def as_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

############################################################
#   Application Models
############################################################
class User(Base):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    passwd = db.Column(db.String())
    is_active = db.Column(db.Boolean())
    user_info = db.relationship('UserInfo', backref=db.backref('users', uselist=False))

    def __init__(self, username, passwd, is_active):
        self.username = username
        self.passwd = generate_password_hash(passwd)
        self.is_active = is_active

    def __repr__(self):
        return '<id {}>'.format(self.id_user)
    
    def get_user_id(self):
        return self.id_user
    
    def set_password(self, password):
        self.passwd = generate_password_hash(password)

    def check_password(self, passwd):
        return check_password_hash(self.passwd, passwd)
    
class UserInfo(Base):
    __tablename__ = 'users_info'
    __table_args__ = (
        db.PrimaryKeyConstraint('id_user'),
    )
    
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user', ondelete='CASCADE'))    
    name = db.Column(db.String())
    lastname = db.Column(db.String())
    email = db.Column(db.String())
    user = db.relationship('User', backref=db.backref('users_info', uselist=False))
    
    def __init__(self, id_user, name, lastname, email):
        self.id_user = id_user
        self.name = name
        self.lastname = lastname
        self.email = email



############################################################
#   oAuth Models
############################################################
class BaseOAuth(db.Model):
    __abstract__  = True

    def as_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

class OAuth2Client(BaseOAuth, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'
    client_id = db.Column(db.String(48), primary_key=True)
    
class OAuth2ClientUsers(BaseOAuth):
    __tablename__ = 'oauth2_client_users'
    __table_args__ = (
        db.PrimaryKeyConstraint('client_id','user_id'),
    )

    client_id = db.Column(
        db.String(48), db.ForeignKey('oauth2_client.client_id', ondelete='CASCADE')
    )
    oauth2client = db.relationship('OAuth2Client')
    
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id_user', ondelete='CASCADE')
    )
    user = db.relationship('User')
    
class VwOAuth2ClientUsers(BaseOAuth, OAuth2ClientMixin):
    __tablename__ = 'vw_oauth2_client_users'
    __table_args__ = (
        db.PrimaryKeyConstraint('client_id','user_id'),
    )
    client_id = db.Column(
        db.String(48), db.ForeignKey('oauth2_client.client_id', ondelete='CASCADE')
    )
    oauth2client = db.relationship('OAuth2Client')
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id_user', ondelete='CASCADE')
    )
    user = db.relationship('User')

class OAuth2Token(BaseOAuth, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id_user', ondelete='CASCADE'))
    user = db.relationship('User')

    def is_refresh_token_expired(self):
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at < time.time()
############################################################