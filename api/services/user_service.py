from flask import current_app, abort, jsonify, make_response
from sqlalchemy import exc
from api.app import db
from api.database.models import User, UserInfo, OAuth2ClientUsers


def build_user_schema(user):
    """Build user data to rest service
    Make Join of Model Users and Users_Info
    """
    mod = {}
    mod['id_user'] = user.id_user
    mod['username'] = user.username
    mod['password'] = user.passwd
    mod['date_created'] = user.date_created
    mod['date_modified'] = user.date_modified
    mod['is_active'] = user.is_active
    user_info = user.user_info
    if len(user_info) > 0:
        mod['name'] = user_info[0].name
        mod['lastname'] = user_info[0].lastname
        mod['email'] = user_info[0].email
    return mod

def get_user(id_user):
    """Get data of the user by id
    """
    user = User.query.get(id_user)
    return build_user_schema(user)


def get_all_users(page, per_page):
    """Get all users
    """
    arr_users = []
    users = User.query.filter_by(is_active=True).order_by(User.id_user).paginate(page,per_page,error_out=False).items
    for user in users:
        mod = build_user_schema(user)
        arr_users.append(mod)
    return arr_users

def save_new_user(data):
    """Create new user
    """
    try:
        #Validate if the username exist
        user = User.query.filter_by(username=data.get('username')).first()
        if user:
            abort(make_response(jsonify({
                    "errors":{
                        "sql":"username exist in DB"
                    },"message":"Username exist"
            }), 409))
            
        #Create user
        user = User(
            username=data.get('username'),
            passwd=data.get('password'),
            is_active=True
        )
        db.session.add(user)
        db.session.flush()
        id_user = user.id_user
        user_info = UserInfo(
            id_user=id_user, 
            name=data.get('name'),
            lastname=data.get('lastname'),
            email=data.get('email')
        )
        db.session.add(user_info)
        oAuthUser = OAuth2ClientUsers(client_id=current_app.config['OAUTH2_CLIENT_ID'],user_id=id_user)
        db.session.add(oAuthUser)
        db.session.commit()
        return make_response(jsonify({
                'id_user': id_user
            }), 201)
    except exc.DBAPIError as e:
        #On error in SQL
        current_app.logger.error('Fail on create user %s' % str(e) )
        db.session().rollback()
        abort(make_response(jsonify({
                "errors":{
                    "sql":"duplicate key value"
                },"message":"Error in database"
        }), 409))


def update_user(id_user, data):
    """Update user
    """
    user = User.query.get(id_user)
    if not user:
        abort(make_response(jsonify({
                "errors":{
                    0:"User not found by the id"
                },"message":"User not found"
        }), 409))
    user.set_password( data.get('password') if data.get('password') else user.passwd )
    ui = user.user_info[0]
    ui.name = data.get('name', ui.name)
    ui.lastname = data.get('lastname', ui.lastname)
    ui.email = data.get('email', ui.email)
    db.session.commit()
    return True

def delete_user(id_user):
    """Delete user by is_active = False
    """
    user = User.query.get(id_user)
    if not user:
        abort(make_response(jsonify({
                "errors":{
                    0:"User not found by the id"
                },"message":"User not found"
        }), 409))
    user.is_active = False
    db.session.commit()
    return True