
def config_app(app):
    """General Configuration in the Flask app
    """
    app.config.from_object('config')
    app.secret_key = app.config['SECRET_KEY']
    app.debug = True
    app.testing  = True
