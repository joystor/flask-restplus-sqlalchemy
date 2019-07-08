from api import app as application
app = application.create_app()
app.run( host=app.config.get('HOST', '0.0.0.0'),
         port=app.config.get('PORT', 5000))
