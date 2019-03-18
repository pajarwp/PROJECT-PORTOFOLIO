import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprint import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import *
from blueprint.user import Users
from blueprint.buyer import Buyers

bp_buyer = Blueprint('buyer', __name__)
api = Api(bp_buyer)

class BuyerResource(Resource):
    @jwt_required
    def get(self, buyer_id=None):
        user = get_jwt_identity()
        identity1 = marshal(user, Users.response_field)
        
        if identity1['status'] == 'admin' :
            if buyer_id == None:
                parse = reqparse.RequestParser()
                parse.add_argument('p',type=int,location='args',default=1)
                parse.add_argument('rp',type=int,location='args',default=5)
                parse.add_argument('buyer_id',location='args')
                parse.add_argument('username',location='args')
                
                args = parse.parse_args()

                offset = args['p']*args['rp']-args['rp']

                qry = Buyers.query

                if args['buyer_id'] is not None:
                    qry = qry.filter(Buyers.buyer_id.like(args['buyer_id']))
                if args['username'] is not None:
                    qry = qry.filter(Buyers.username.like("%"+args['username']+"%"))
                
                buyer_lists = []
                for buyer in qry.limit(args['rp']).offset(offset).all():
                    data = marshal(buyer, Buyers.response_field)
                    buyer_data = {
                        'buyer_id' : data['buyer_id'],
                        'username' : data['username'],
                        'email' : data['email'],
                        'status' : data['status'],
                    }
                    buyer_lists.append(buyer_data)                
                return buyer_lists, 200, {'Content-Type': 'application/json'}
            else:
                qry = Buyers.query.get(buyer_id)
                data = marshal(qry, Buyers.response_field)
                buyer_data = {
                    'buyer_id' : data['buyer_id'],
                    'username' : data['username'],
                    'email' : data['email'],
                    'status' : data['status'],
                }                    

                if qry is not None:
                    return buyer_data
                return {'status': 'NOT FOUND','message':'Buyer not found'}, 404, {'Content-Type':'application/json'}
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', location='json', required=True)
        parse.add_argument('contact', location='json', required=True)
        parse.add_argument('email', location='json', required=True)
        parse.add_argument('password', location='json', required=True)

        args = parse.parse_args()

        buyers = Buyers(None, args['username'], args['contact'], args['email'], args['password'], 'buyer')

        db.session.add(buyers)
        db.session.commit()

        return marshal(buyers, Buyers.response_field), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self):
        buyer = get_jwt_identity()
        identity = marshal(buyer, Buyers.response_field)

        if identity['status'] == 'buyer' :
            parse = reqparse.RequestParser()
            parse.add_argument('username', location='json', required=True)
            parse.add_argument('contact', location='json', required=True)
            parse.add_argument('email', location='json', required=True)
            parse.add_argument('password', location='json', required=True)

            args = parse.parse_args()

            qry = Buyers.query.get(identity['buyer_id'])
            if qry is None:
                return {'status': 'NOT FOUND','message':'Buyer not found'}, 404, {'Content-Type':'application/json'}
            else:    
                qry.username = args['username']
                qry.contact = args['contact']
                qry.email = args['email']
                qry.password = args['password']

                db.session.commit()

                return marshal(qry, Buyers.response_field), 200, {'Content-Type': 'application/json'}
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }
            
    @jwt_required
    def delete(self, buyer_id=None):
        buyer = get_jwt_identity()
        identity1 = marshal(buyer, Buyers.response_field)
        user = get_jwt_identity()
        identity2 = marshal(user, Users.response_field)
        if identity1['status'] == 'buyer' :
            qry = Buyers.query.get(identity1['buyer_id'])
            if qry is None:
                return {'status': 'NOT FOUND','message':'Buyer not found'}, 404, {'Content-Type':'application/json'}        
            else:
                db.session.delete(qry)
                db.session.commit()
                return ("Deleted")
        elif identity2['status'] == 'admin':
            qry = Buyers.query.get(buyer_id)
            if qry is None:
                return {'status': 'NOT FOUND','message':'Buyer not found'}, 404, {'Content-Type':'application/json'}        
            else:
                db.session.delete(qry)
                db.session.commit()
                return ("Deleted")                
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }


class SelfResource(Resource):
    @jwt_required
    def get(self):
        buyer = get_jwt_identity()
        identity2 = marshal(buyer, Buyers.response_field)
        
        if identity2['status'] == 'buyer':
            qry = Buyers.query.get(identity2['buyer_id'])
            if qry is not None:
                return marshal(qry, Buyers.response_field)
            return {'status': 'NOT FOUND','message':'Buyer not found'}, 404, {'Content-Type':'application/json'}
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }
api.add_resource(BuyerResource,'/buyer', '/buyer/<int:buyer_id>')
api.add_resource(SelfResource,'/buyer_profile')