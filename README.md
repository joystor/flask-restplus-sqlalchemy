# Flask-restplus-sqlalchemy

## Objectives

With this project you can undestand the basic use of Flask, flask-restplus, Flask-SQLAlchemy, this cases are in the code an you can explore or use it as template for REST-API application.

## Why other Flask template

I want to lear Flask, and I have troubles resolving basic problems like adding oAuth2.0 Field validations and other described next:

### Flask
 - Aplication configuration
 - Configure Logger
 - Integrate with database
 - Propose of the application structure
 - Restrict access with oAuth2 in config

### Flask-SQLAlchemy
 - Using Joins
 - Use paginator
 - CRUD with models

### flask-restplus
 - Create routes
 - Model-Schema validation
 - Custom Fields (Email validation)
 - Using decorators to document routes in swagger API-DOC

### pytest
 - Global variables and use of cookies

## Project base structure
```
├── README.md
├── api                     # Path to api
│   ├── app.py              # application creation
│   ├── app_config.py       # application load configurations
│   ├── app_events.py       # load flask events to application
│   ├── app_logger.py       # configure applicaiont logger
│   ├── commands            # path to store flask commands
│   │   └── db_admin.py     # flask commands with default values (Users and oAuth2.0 client_id)
│   ├── database            # database models and function
│   │   ├── __init__.py
│   │   └── models.py
│   ├── mod_auth            # configuration and routes for security in oAuth2.0 only password grant configured
│   │   ├── __init__.py
│   │   ├── oauth2.py
│   │   └── routes.py
│   └── routes              # add all routes of the application 
│   │   ├── __init__.py     # this merge all routes in the other files in routes
│   │   ├── index_route.py
│   │   ├── me_route.py
│   │   └── users_route.py
│   └── services            # Database logic called in routes
│   │   ├── user_serice.py   
│   └── utils               # Scripts used by custom files validations
│       ├── custom_fields.py
│       └── validator.py
├── test                    # Test scripts
│   ├── conftest.py         # File configuration of pytest
|   └── test_#.py           # Test case order by number file
├── config.py               # configuration of the aplication, database url, api path, doc swagger path
├── requirements.txt        # requirements for pip install
├── run.py                  # scritp to run app without gunicorn $ python run.py
└── wsgi.py                 # script to run with gunicorn $ gunicorn --bind 0.0.0.0:5000 wsgi:app
```

## Prepare application
```
$ python3 -m venv env
$ source env/bin/activate    # in windows $ env\Scripts\activate.bat
$ pip install -r requirements.txt
$ gunicorn --bind 0.0.0.0:5000 wsgi:app 

#Exit of the enviroment
$ deactivate
```

## Before start execute this flask commands in app/commands
```
$ flask create-tables
$ flask add-default-values   # this add default values configured in api/commands/db_admin.py
```

## Run aplication
You can run this aplication with gunicorn
```
$ gunicorn --bi nd 0.0.0.0:5000 wsgi:app 
```
or by Python run script
```
$ python run.py
```
or
```
$ flask run
```

### oAuth login 
```
curl -i -b cookie-flask.txt -XPOST http://127.0.0.1:5000/oauth/login -d "username=admin&password=mypwdz&client_id=WfR1rhmADab4QS11L7mx1dHH"

Response:
{
  "client_secret": "ZWuhD0pD4xgX5vlaG1TNogQy02KTxr6LBBbbZp4ivGVqmDxg"
}


curl -i -b cookie-flask.txt -XPOST http://127.0.0.1:5000/api/me_ses
```



### oAuth login to get Token
```
curl -i -b cookie-flask.txt -u WfR1rhmADab4QS11L7mx1dHH:ZWuhD0pD4xgX5vlaG1TNogQy02KTxr6LBBbbZp4ivGVqmDxg -XPOST http://127.0.0.1:5000/oauth/token -d "grant_type=password&username=admin&password=mypwdz"

Response:
{
  "access_token": "3zDqSFA4AN82VxPjh0kX1vleNqWIUrvu24IsbxOBZv", "expires_in": 864000, "refresh_token": "RVYfEnKNQSGjMWT6hrbMx6q83CCmLQ8i01NuQ1EffNaqQjHn", "token_type": "Bearer"
}

curl -i -H "Authorization: Bearer 2b5muftN9mh0sBr9hnfHc15zU6CRCIxS22qxVoGjz2" -b cookie-flask.txt http://127.0.0.1:5000/api/me
```

With this token youu can access to the swagger documentation:  http://127.0.0.1:5000/rest/v1/docs/ click on the Authorize button and paste the token like the next example:


Bearer 2b5muftN9mh0sBr9hnfHc15zU6CRCIxS22qxVoGjz2


### Testing

The base test scrit store the token to test all services

```
coverage run -m pytest -s
coverage report
coverage html 
``` 

To see report html 
```
cd htmlcov
python -m http.server 5000
```