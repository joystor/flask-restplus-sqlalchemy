from flask import Flask, Blueprint
from flask_restplus import Api, apidoc
from api.routes.index_route import add_index
from api.routes.users_route import add_users
from api.routes.me_route import add_my_info

def add_routes(app):
    authorizations = {
        'oauth2': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        },
    }
    #routes 
    bp_main = Blueprint("main_v"+app.config['API_VERSION'], __name__)
    api_main = Api(bp_main)
    add_index(api_main)
    app.register_blueprint(bp_main, url_prefix="/")
    
    #routes in API_PREFIX_URL
    blueprint = Blueprint("v"+app.config['API_VERSION'], __name__)
    api = Api(blueprint, 
              doc=app.config['API_DOC_URL'], 
              version=app.config['API_VERSION'], 
              authorizations=authorizations
              )
    add_users(api)
    add_my_info(api)
    app.register_blueprint(blueprint, url_prefix=app.config['API_PREFIX_URL'])