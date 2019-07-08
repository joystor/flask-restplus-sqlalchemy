from flask import current_app, request, abort, jsonify, make_response
from flask_restplus import Namespace, Resource, fields, marshal
from api.utils import custom_fields, validator
from api.services.user_service import get_user, get_all_users, save_new_user, delete_user, update_user

import json, re

def add_users(api):    
    
    #User Schema
    user_schema = api.model('User', {
        'id_user': fields.Integer(required=False, description='ID of the user', readonly=True),
        'username': fields.String(required=True, description='Username of the user'),
        'name': fields.String(required=True, description='Name of the user'),
        'lastname': fields.String(required=False, description='Lastname of the user'),
        'email': custom_fields.Email(required=False, description='Email of the user'),
        'password': fields.String(required=True, description='Password of the user'),
        'date_created': custom_fields.DateTime(required=False, description='Date created of the record', readonly=True),
        'date_modified': custom_fields.DateTime(required=False, description='Date modified of the record', readonly=True),
        'is_active': fields.Boolean(required=False, description='User active or not', readonly=True)
    })
    
    
    ns = api.namespace('users', description='Users CRUD operations', authorizations=api.authorizations)
    
    @ns.route("/")
    class UserNewRoute(Resource):
        @api.expect(user_schema, validate=True, envelope='json')
        @api.doc(security='oauth2', responses={
            201: 'User successfully created',
            409: 'Conflict, user already exists',
            422: 'Validation Error'
        })
        @api.marshal_with(user_schema, mask="id_user")
        def post(self):
            """Creates a new User """
            #Validate data
            validator.validate_payload(request.json, user_schema)
            return save_new_user(data=request.json)
    
    
    @ns.route("/<int:page>/<int:per_page>")
    class UsersRoute(Resource):

        @api.marshal_with(user_schema, as_list=True, 
                    mask="id_user,username,name,lastname,email,date_created,date_modified")
        @api.response(200, 'Active users list')
        @api.doc(security='oauth2')
        def get(self, page=1, per_page=2):
            """List users usign paginator"""
            return get_all_users(page, per_page)
            
            
    @ns.route("/<int:id_user>")
    class UserRoute(Resource):
        
        @api.marshal_with(user_schema,
                    mask="id_user,username,name,lastname,email,date_created,date_modified")
        @api.response(200, 'User info')
        @api.doc(security='oauth2')
        def get(self, id_user):
            """List User info"""
            return get_user(id_user)
        
        @api.doc(security='oauth2', responses={
            201: 'User successfully deleted'})
        def delete(self, id_user):
            '''Delete user by id_user'''
            delete_user(id_user)
            return '', 201
        
        @api.expect(user_schema, envelope='json', validate=False)
        @api.doc(security='oauth2', responses={
            201: 'User successfully updated',
            422: 'Validation Error'})
        def put(self, id_user):
            '''Update user by id_user'''
            validator.validate_payload(request.json, user_schema, validate_required=False)
            update_user(id_user=id_user, data=request.json )
            return '', 201