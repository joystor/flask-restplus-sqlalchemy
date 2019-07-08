from flask_restplus import Resource
from authlib.flask.oauth2 import current_token
from api.mod_auth.oauth2 import authorization#, require_oauth
from api.database.models import User

def add_my_info(api):
    
    @api.route('/me')
    class MyInfo(Resource):
        def get(self):
            user = current_token.user
            return {'hello': user.username}