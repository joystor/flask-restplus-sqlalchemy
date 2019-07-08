from flask import Flask, session
from flask_session import Session
from api.database import db
from .routes import add_routes
from .app_config import config_app
from .app_logger import config_logger
from .app_events import register_events
from .mod_auth.oauth2 import config_oauth
from .mod_auth.routes import bp_oauth2
from .commands.db_admin import add_db_admin_cmds

def create_app(package_name='Yggdrasil'):
    """Create the Flask application
    """
    #Configure core app
    app = Flask(package_name)
    config_app(app)
    config_logger(app)
    Session(app)
    
    #Adding routes
    db.init_app(app)
    add_routes(app)
    config_oauth(app)
    app.register_blueprint(bp_oauth2, url_prefix='')
    
    #Adding commands
    add_db_admin_cmds(app, db)
    
    #Adding applications events
    register_events(app, db)
    return app