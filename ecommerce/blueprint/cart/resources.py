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
                    data = marshal(data, Carts.response_field)
                    item = qry2.get(data['item_id'])
                    item = marshal(item, Items.response_field)
                    total_price = total_price + data['total_price']                
                    detail = { item['item_name']: data['item_sum']}
                    list_item.append(detail)
                dict_item = {'list_item' : list_item}
                cart.append(dict_item)
                total = {'total_payment' : total_price}
                cart.append(total)
                return cart, 200, {'Content-Type': 'application/json'}
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }

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

            carts = Carts(None, identity['buyer_id'], args['item_id'], args['item_sum'], (qry.price * args['item_sum']))

            db.session.add(carts)
            db.session.commit()

            return marshal(carts, Carts.response_field), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self, cart_id):
        buyer = get_jwt_identity()
        identity = marshal(buyer, Buyers.response_field)

        if identity['status'] == 'buyer' :
            parse = reqparse.RequestParser()
            parse.add_argument('item_id', location='json', type=int, required=True)
            parse.add_argument('item_sum', location='json', type=int, required=True)

            args = parse.parse_args()

            qry1 = Carts.query.get(cart_id)
            qry2 = Items.query.get(args['item_id'])
            if qry2 is None :
                return {'status': 'NOT FOUND','message':'Item not found'}, 404, {'Content-Type':'application/json'}
            else :
                if qry1 is None:
                    return {'status': 'NOT FOUND','message':'Cart not found'}, 404, {'Content-Type':'application/json'}
                elif qry1 is not None and qry1.buyer_id != identity['buyer_id'] :
                    return {'status': 'NOT FOUND','message':'Unautorized User'}, 404, {'Content-Type':'application/json'}
                else:    
                    qry1.item_id = args['item_id']
                    qry1.item_sum = args['item_sum']
                    qry1.total_price = (args['item_sum'] * qry2.price)

                    db.session.commit()

                    return marshal(qry1, Carts.response_field), 200, {'Content-Type': 'application/json'}
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }
            
    @jwt_required
    def delete(self, cart_id=None):
        buyer = get_jwt_identity()
        identity = marshal(buyer, Buyers.response_field)
        if identity['status'] == 'buyer' :
            qry = Carts.query.get(cart_id)
            if qry is None:
                return {'status': 'NOT FOUND','message':'Cart not found'}, 404, {'Content-Type':'application/json'}        
            elif qry is not None and qry.buyer_id != identity['buyer_id'] :
                return {'status': 'NOT FOUND','message':'Unautorized Buyer'}, 404, {'Content-Type':'application/json'}            
            else:
                db.session.delete(qry)
                db.session.commit()
                return ("Deleted")             
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }
    
api.add_resource(CartResource,'/my_cart', '/my_cart/<int:cart_id>')
