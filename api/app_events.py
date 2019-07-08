from flask import request, session, jsonify, abort
from api.mod_auth.oauth2 import require_oauth
from authlib.oauth2 import OAuth2Error
import time

def register_events(app, db):
    
    #@app.before_first_request
    #def before_first_req():
    #    """Function trigged on the first request of the application
    #    """

    @app.before_request
    def before_request():
        """Function to dectect any request and verify if is protected
        
           Variables in config.py
           OAUTH_EXCEPT_PROTECTED_ROUTES áths to omit the verification
           OAUTH_PROTECTED_ROUTES   paths protected by oAuth
        """
        path = request.path
        app.logger.info("%s",path)
        if not path.startswith(tuple(app.config['OAUTH_EXCEPT_PROTECTED_ROUTES'])):
            if path.startswith(tuple(app.config['OAUTH_PROTECTED_ROUTES'])):
                is_logged = False
                try:
                    with require_oauth.acquire() as token:
                        expired = token.get_expires_at() - int(time.time())
                        app.logger.info("  token:%i", expired)
                        if expired < 0:
                            app.logger.info("  token expired")
                            return abort(401, 'TOKEN expired')
                        is_logged = True
                    if is_logged == False:
                        return abort(401, 'TOKEN not valid')
                except Exception as error:
                    app.logger.error("  Error to get token %s",error)
                    return abort(401, 'Authorization requiered')
       
       
    @app.after_request
    def add_header(resp):
        """Function triggered when the request is finish, in this case to prevent cache
        """
        resp.headers['Cache-Control'] = 'no-store'
        resp.headers['Pragma'] = 'no-cache'
        return resp

    ####################################################################### 
    @app.errorhandler(500)
    def internal_server_error(e):
        """Handling Errors 500
        """
        response = jsonify(
            error=e.message,
            error_description="Error 500")
        return response, 500

    """Other errors
    @app.errorhandler(DatabaseError)
    def special_exception_handler(error):
        return 'Database connection failed', 500
    """