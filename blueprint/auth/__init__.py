import logging, json, hashlib
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_cors import CORS
from ..user import Users
from ..buyer import Buyers

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)
CORS(bp_auth)
class CreateTokenUserResources(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('store_name', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()
        password = hashlib.md5(args['password'].encode()).hexdigest()

        user = Users.query.filter_by(store_name = args['store_name']).filter_by(password = password).first()
        
        if user is not None:
            qry = marshal(user, Users.response_field)
            data = {
                'user_id' : qry['user_id'],
                'store_name' : qry['store_name'],
                'status' : qry['status']
            }
            token = create_access_token(identity = data)
        else:
            return {'status':'UNAUTORIZED', 'message':'wrong store name or password'}, 401
        return {'status': 'success', 'message': 'logged in', 'data': qry, 'token': token}, 200

class CreateTokenBuyerResources(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()
        password = hashlib.md5(args['password'].encode()).hexdigest()

        buyer = Buyers.query.filter_by(username = args['username']).filter_by(password = password).first()
        
        if buyer is not None:
            qry = marshal(buyer, Buyers.response_field)
            data = {
                'buyer_id' : qry['buyer_id'],
                'username' : qry['username'],
                'status' : qry['status']
            }
            token = create_access_token(identity = data)
        else:
            return {'status':'UNAUTORIZED', 'message':'wrong username or password'}, 401
        return {'status':'success', 'message':'logged in', 'data': qry ,'token': token}, 200

api.add_resource(CreateTokenUserResources, '/login/user')
api.add_resource(CreateTokenBuyerResources, '/login/buyer')

