import logging, json, hashlib
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprint import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import *
from blueprint.user import Users
from blueprint.buyer import Buyers

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UserResource(Resource):
    def __init__(self):
        if Users.query.first() is None:
            users = Users(None, 'superuser', 'admin@gmail.com', hashlib.md5('jar'.encode()).hexdigest(), 'admin')
            db.session.add(users)
            db.session.commit()

    def get(self, user_id=None):
        if user_id == None:
            parse = reqparse.RequestParser()
            parse.add_argument('user_id',location='args')
            parse.add_argument('username',location='args')
            
            args = parse.parse_args()
            qry = Users.query
            if args['user_id'] is not None :
                qry = qry.filter(Users.user_id.like(args['user_id']))                  
            if args['username'] is not None:
                qry = qry.filter(Users.username.like("%"+args['username']+"%"))
            user_lists = []
            for user in qry:
                data = marshal(user, Users.response_field)
                user_data = {
                    'user_id' : data['user_id'],
                    'username' : data['username'],
                    'email' : data['email'],
                    'status' : data['status'],
                }
                user_lists.append(user_data)
            return {'status':'success','data':user_lists}, 200, {'Content-Type': 'application/json'}
        else:
            qry = Users.query.get(user_id)
            data = marshal(qry, Users.response_field)
            user_data = {
                'user_id' : data['user_id'],
                'username' : data['username'],
                'email' : data['email'],
                'status' : data['status'],
            }                    
            if qry is not None:
                return user_data
            return {'status': 'NOT FOUND','message':'User not found'}, 404, {'Content-Type':'application/json'}                

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', location='json', required=True)
        parse.add_argument('email', location='json', required=True)
        parse.add_argument('password', location='json', required=True)

        args = parse.parse_args()
        password = hashlib.md5(args['password'].encode()).hexdigest()
        users = Users(None, args['username'], args['email'], password, 'user')

        db.session.add(users)
        db.session.commit()
        data = marshal(users, Users.response_field)
        return {'status':'success', 'message':"user's data saved", 'data': data}, 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self):
        user = get_jwt_identity()
        identity = marshal(user, Users.response_field)

        if identity['status'] == 'user':
            parse = reqparse.RequestParser()
            parse.add_argument('username', location='json', required=True)
            parse.add_argument('email', location='json', required=True)
            parse.add_argument('password', location='json', required=True)

            args = parse.parse_args()
            password = hashlib.md5(args['password'].encode()).hexdigest()

            qry = Users.query.get(identity['user_id'])
            if qry is None:
                return {'status': 'NOT FOUND','message':'User not found'}, 404, {'Content-Type':'application/json'}
            else:    
                qry.username = args['username']
                qry.email = args['email']
                qry.password = password

                db.session.commit()
                data = marshal(qry, Users.response_field)
                return {'status':'success', 'message':"User's data edited", 'data': data}, 200, {'Content-Type': 'application/json'}
        else:
            return {'status':'UNAUTORIZED', 'message':'unautorized user'}, 401, { 'Content-Type': 'application/json' }
            
    @jwt_required
    def delete(self, user_id=None):
        user = get_jwt_identity()
        identity = marshal(user, Users.response_field)

        if identity['status'] == 'user':
            qry = Users.query.get(identity['user_id'])
            if qry is None:
                return {'status': 'NOT FOUND','message':'User not found'}, 404, {'Content-Type':'application/json'}        
            else:
                db.session.delete(qry)
                db.session.commit()
                data = marshal(qry, Users.response_field)
                return {'status': 'success','message':"User's data deleted", 'data': data}, 200, {'Content-Type':'application/json'}        
        elif identity['status'] == 'admin':
            qry = Users.query.get(user_id)
            if qry is None:
                return {'status': 'NOT FOUND','message':'User not found'}, 404, {'Content-Type':'application/json'}        
            else:
                db.session.delete(qry)
                db.session.commit()
                data = marshal(qry, Users.response_field)
                return {'status': 'success','message':"User's data deleted", 'data': data}, 200, {'Content-Type':'application/json'}        
        else:
            return {'status':'UNAUTORIZED', 'message':'unautorized user'}, 401, { 'Content-Type': 'application/json' }

class SelfResource(Resource):
    @jwt_required
    def get(self, user_id=None):
        user = get_jwt_identity()
        identity = marshal(user, Users.response_field)
        if identity['status'] == 'user':
            qry = Users.query.get(identity['user_id'])
            data = marshal(qry, Users.response_field)
            if qry is not None:
                return {'status':'success', 'data': data}, 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT FOUND','message':'User not found'}, 404, {'Content-Type':'application/json'}
        else:
            return {'status':'UNAUTORIZED', 'message':'unautorized user'}, 401, { 'Content-Type': 'application/json' }

api.add_resource(UserResource,'/user', '/user/<int:user_id>')
api.add_resource(SelfResource,'/user_profile')