import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprint import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS
from sqlalchemy import desc
from blueprint.cart import Carts
from blueprint.buyer import Buyers
from . import *

bp_transaction = Blueprint('transaction', __name__)
api = Api(bp_transaction)
CORS(bp_transaction)
class TransactionResource(Resource) :
    @jwt_required
    def post(self):
        buyer = get_jwt_identity()
        identity = marshal(buyer, Buyers.response_field)
        
        if identity['status'] == 'buyer' :
            qry = Carts.query
            qry1 = Transactions.query
            sort = qry.filter(Carts.buyer_id.like(identity['buyer_id']))
            sort2 = qry1.first()
            if sort is not None :
                total_price = 0
                for data in sort :
                    if data.transaction_id == 0 :
                        total_price = total_price + data.total_price
                        if sort2 is None :
                            cart = Carts.query.get(data.cart_id)
                            cart.transaction_id = 1
                            db.session.commit()
                        else :
                            cart = Carts.query.get(data.cart_id)
                            transaction = Transactions.query.order_by(desc(Transactions.transaction_id)).first()
                            cart.transaction_id = transaction.transaction_id + 1
                            db.session.commit()
                if total_price > 0 :            
                    transactions = Transactions(None, identity['buyer_id'], total_price)
                    db.session.add(transactions)
                    db.session.commit()
                    data = marshal(transactions, Transactions.response_field)
                    return {'status':'transaction successful','data':data}, 200, {'Content-Type': 'application/json'}

                else :
                    return {'status':'transaction failed'}, 200, {'Content-Type': 'application/json'}

    @jwt_required
    def get(self, transaction_id=None):
        buyer = get_jwt_identity()
        identity = marshal(buyer, Buyers.response_field)
        
        if identity['status'] == 'buyer' :
            if transaction_id is None:
                parser = reqparse.RequestParser()
                parser.add_argument('p', type=int, location='args', default=1)
                parser.add_argument('rp', type=int, location='args', default=5)
        
                args = parser.parse_args()

                offset = (args['p'] * args['rp']) - args['rp']

                qry = Transactions.query

                rows = []
                for row in qry:
                    if row.buyer_id == identity['buyer_id'] :
                        rows.append(marshal(row, Transactions.response_field))
                return {'status':'success','data':rows}, 200, {'Content-Type': 'application/json'}

            else:
                qry = Transactions.query.get(transaction_id)
                data = marshal(qry, Transactions.response_field)
                if qry.buyer_id != identity['buyer_id'] :
                    return {'status':'UNAUTORIZED', 'message':'unautorized buyer'}, 401, { 'Content-Type': 'application/json' }
                if qry is not None:
                    return {'status':'success','data':data}, 200, {'Content-Type': 'application/json'}
                else:
                    return {'status': 'NOT FOUND','message':'Transaction not found'}, 404, {'Content-Type':'application/json'}

api.add_resource(TransactionResource,'/transaction', '/transaction/<int:transaction_id>')
