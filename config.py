#Application config
import os
os.environ['FLASK_DEBUG'] = '1'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
THREADS_PER_PAGE = 2

#generate secret key with 
# $ python -c 'import os; print(os.urandom(16))'
SECRET_KEY = b"<\xb7JL\x91Y\x8c\x9c<\x03'\xbc\xb9C\xa7\xa1"

#Session Config
SESSION_TYPE='filesystem'
os.makedirs(os.path.join(BASE_DIR,'tmp_sessions') , exist_ok=True)
SESSION_FILE_DIR= os.path.join(BASE_DIR,'tmp_sessions') 

#API Configuration
API_VERSION = "1.0"
API_PREFIX_URL = "/rest/v1"
API_DOC_URL = "/docs/"
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False


#oAuth server
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'
OAUTH2_CLIENT_ID = 'WfR1rhmADab4QS11L7mx1dHH'
OAUTH2_CLIENT_SECRET = 'ZWuhD0pD4xgX5vlaG1TNogQy02KTxr6LBBbbZp4ivGVqmDxg'
OAUTH2_REFRESH_TOKEN_GENERATOR = True
OAUTH_PROTECTED_ROUTES = [
    "/rest/",
]
OAUTH_EXCEPT_PROTECTED_ROUTES = [
    API_PREFIX_URL + "/swagger.json",
    API_PREFIX_URL + API_DOC_URL,
    "/swaggerui/",
]

#DB Configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO=False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'flask_main.db')
