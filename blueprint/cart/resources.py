import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprint import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import *
from blueprint.item import Items
from blueprint.buyer import Buyers

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class CartResource(Resource):
    @jwt_required
    def get(self):
        buyer = get_jwt_identity()
        identity = marshal(buyer, Buyers.response_field)
        
        if identity['status'] == 'buyer':
            qry = Carts.query
            sort = qry.filter(Carts.buyer_id.like(identity['buyer_id']))
            qry2 = Items.query
            if sort is not None:
                cart = []
                list_item = []
                total_price = 0
                for data in sort :
                    if data.transaction_id == 0 :
                        data = marshal(data, Carts.response_field)
                        item = qry2.get(data['item_id'])
                        item = marshal(item, Items.response_field)
                        total_price = total_price + data['total_price']
                        item_dict = {
                            'item_id' : item['item_id'],
                            'item_name' : item['item_name'],
                            'category' : item['category'],
                            'price' : item['price'],
                            'size' : item['size'],
                            'color' : item['color'],
                            'posted_by' : item['posted_by'],
                            'qty' : data['item_sum'],
                        }                
                        list_item.append(item_dict)
                return {'status':'success', 'list_item': list_item, 'total_payment':total_price}, 200, {'Content-Type': 'application/json'}
        else:
            return {'status':'UNAUTORIZED', 'message':'unautorized user'}, 401, { 'Content-Type': 'application/json' }

    @jwt_required
    def post(self):
        buyer = get_jwt_identity()
        identity = marshal(buyer, Buyers.response_field)
        
        if identity['status'] == 'buyer' :
            parse = reqparse.RequestParser()
            parse.add_argument('item_id', location='json', type=int, required=True)
            parse.add_argument('item_sum', location='json', type=int, required=True)

            args = parse.parse_args()

            qry = Items.query.get(args['item_id'])
            
            if qry.qty < args['item_sum'] :
                return {'status':'Request failed','message':'Not Enough Stock'}, 405, { 'Content-Type': 'application/json' }
            else :
                carts = Carts(None, identity['buyer_id'], args['item_id'], args['item_sum'], (qry.price * args['item_sum']), 0)
                qry.qty = (qry.qty - args['item_sum'])
                db.session.add(carts)
                db.session.commit()
                data = marshal(carts, Carts.response_field)

                return {'status':'success', 'message':"Item added to cart", 'data': data}, 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self, cart_id):
        buyer = get_jwt_identity()
        identity = marshal(buyer, Buyers.response_field)

        if identity['status'] == 'buyer' :
            parse = reqparse.RequestParser()
            parse.add_argument('item_sum', location='json', type=int, required=True)

            args = parse.parse_args()

            qry1 = Carts.query.get(cart_id)
            qry2 = Items.query.get(qry1.item_id)
            if qry2 is None :
                return {'status': 'NOT FOUND','message':'Item not found'}, 404, {'Content-Type':'application/json'}
            else :
                if qry1 is None:
                    return {'status': 'NOT FOUND','message':'Cart not found'}, 404, {'Content-Type':'application/json'}
                elif qry1 is not None and qry1.buyer_id != identity['buyer_id'] :
                    return {'status': 'NOT FOUND','message':'Unautorized User'}, 404, {'Content-Type':'application/json'}
                elif (qry2.qty + qry1.item_sum) < args['item_sum'] :
                    return {'status':'Request failed','message':'Not Enough Stock'}, 405, { 'Content-Type': 'application/json' }
                elif qry1.transaction_id != 0 :
                    return {'status':'NOT FOUND','message':'Cart already paid'}, 404, { 'Content-Type': 'application/json' }
                else:
                    qry2.qty = ((qry2.qty + qry1.item_sum) - args['item_sum'])     
                    qry1.item_sum = args['item_sum']
                    qry1.total_price = (args['item_sum'] * qry2.price)
                    db.session.commit()
                    data = marshal(qry1, Carts.response_field)

                    return {'status':'success', 'message':"Cart's data edited", 'data': data}, 200, {'Content-Type': 'application/json'}
        else:
            return {'status':'UNAUTORIZED', 'message':'unautorized user'}, 401, { 'Content-Type': 'application/json' }
            
    @jwt_required
    def delete(self, cart_id=None):
        buyer = get_jwt_identity()
        identity = marshal(buyer, Buyers.response_field)
        if identity['status'] == 'buyer' :
            qry = Carts.query.get(cart_id)
            qry2 = Items.query.get(qry.item_id)
            if qry is None:
                return {'status': 'NOT FOUND','message':'Cart not found'}, 404, {'Content-Type':'application/json'}        
            elif qry is not None and qry.buyer_id != identity['buyer_id'] :
                return {'status': 'NOT FOUND','message':'Unautorized Buyer'}, 404, {'Content-Type':'application/json'}            
            elif qry.transaction_id != 0 :
                return {'status':'NOT FOUND','message':'Cart already paid'}, 404, { 'Content-Type': 'application/json' }
            else:
                qry2.qty = (qry2.qty + qry.item_sum)     
                db.session.delete(qry)
                db.session.commit()
                data = marshal(qry, Carts.response_field)
                return {'status': 'success','message':"Cart's data deleted", 'data': data}, 200, {'Content-Type':'application/json'}        
        else:
            return {'status':'UNAUTORIZED', 'message':'unautorized user'}, 401, { 'Content-Type': 'application/json' }

class TransactionDetailResource(Resource):
    @jwt_required
    def get(self, transaction_id):
        buyer = get_jwt_identity()
        identity = marshal(buyer, Buyers.response_field)
        
        if identity['status'] == 'buyer':
            qry = Carts.query
            sort = qry.filter(Carts.buyer_id.like(identity['buyer_id'])).filter(Carts.transaction_id.like(transaction_id))
            qry2 = Items.query
            if sort is None :
                return {'status': 'NOT FOUND','message':'Transaction detail not found'}, 404, {'Content-Type':'application/json'}                
            if sort is not None:
                cart = []
                list_item = []
                total_price = 0
                for data in sort :
                    if data.transaction_id != 0 :
                        data = marshal(data, Carts.response_field)
                        item = qry2.get(data['item_id'])
                        item = marshal(item, Items.response_field)
                        total_price = total_price + data['total_price']
                        item_dict = {
                            'item_id' : item['item_id'],
                            'item_name' : item['item_name'],
                            'category' : item['category'],
                            'price' : item['price'],
                            'size' : item['size'],
                            'color' : item['color'],
                            'posted_by' : item['posted_by'],
                            'qty' : data['item_sum'],
                        }                
                        list_item.append(item_dict)
                return {'status':'success', 'list_item': list_item, 'total_payment':total_price}, 200, {'Content-Type': 'application/json'}
        else:
            return {'status':'UNAUTORIZED', 'message':'unautorized user'}, 401, { 'Content-Type': 'application/json' }    
api.add_resource(CartResource,'/my_cart', '/my_cart/<int:cart_id>')
api.add_resource(TransactionDetailResource,'/transaction_detail/<int:transaction_id>')

