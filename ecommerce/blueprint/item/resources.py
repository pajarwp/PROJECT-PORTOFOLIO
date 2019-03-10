import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprint import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprint.user import Users
from . import *

bp_item = Blueprint('item', __name__)
api = Api(bp_item)

class ItemResource(Resource):
    def get(self, item_id=None):
        if item_id == None:
            parse = reqparse.RequestParser()
            parse.add_argument('p',type=int,location='args',default=1)
            parse.add_argument('rp',type=int,location='args',default=5)
            parse.add_argument('item_name',location='args')
            parse.add_argument('max_price', type=int, location='args')
            parse.add_argument('category',location='args')
            parse.add_argument('size',location='args')
            parse.add_argument('color',location='args')
            parse.add_argument('posted_by',location='args')
          
            args = parse.parse_args()
            offset = args['p']*args['rp']-args['rp']
            qry = Items.query
            if args['item_name'] is not None:
                qry = qry.filter(Items.item_name.like("%"+args['item_name']+"%"))                  
            if args['category'] is not None:
                qry = qry.filter(Items.category.like(args['category']))
            if args['size'] is not None:
                qry = qry.filter(Items.size.like(args['size']))
            if args['color'] is not None:
                qry = qry.filter(Items.color.like(args['color']))
            if args['posted_by'] is not None:
                qry = qry.filter(Items.posted_by.like("%"+args['posted_by']+"%"))    
            item_lists = []
            for item_list in qry.limit(args['rp']).offset(offset).all():
                item = marshal(item_list, Items.response_field)
                if args['max_price'] is not None:
                    if item['price'] <= args['max_price'] :
                        item_lists.append(item)
                else :
                    item_lists.append(item)
            return item_lists, 200, {'Content-Type': 'application/json'}
        else:
            qry = Items.query.get(item_id)
            if qry is not None:
                return marshal(qry, Items.response_field)
            return {'status': 'NOT FOUND','message':'Item not found'}, 404, {'Content-Type':'application/json'}

    @jwt_required
    def post(self):
        user = get_jwt_identity()
        identity = marshal(user, Users.response_field)

        if identity['status'] == 'user':
            parse = reqparse.RequestParser()
            parse.add_argument('item_name', location='json', required=True)
            parse.add_argument('category', location='json', required=True)
            parse.add_argument('price', location='json', type=int, required=True)
            parse.add_argument('size', location='json', required=True)
            parse.add_argument('color', location='json', required=True)

            args = parse.parse_args()

            items = Items(None, args['item_name'], args['category'], args['price'], args['size'], args['color'], identity['username'])

            db.session.add(items)
            db.session.commit()

            return marshal(items, Items.response_field), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self, item_id):
        user = get_jwt_identity()
        identity = marshal(user, Users.response_field)

        if identity['status'] == 'user':
            parse = reqparse.RequestParser()
            parse.add_argument('item_name', location='json', required=True)
            parse.add_argument('category', location='json', required=True)
            parse.add_argument('price', location='json', type=int, required=True)
            parse.add_argument('size', location='json', required=True)
            parse.add_argument('color', location='json', required=True)

            args = parse.parse_args()

            qry = Items.query.get(item_id)
            if qry is None :
                return {'status': 'NOT FOUND','message':'Item not found'}, 404, {'Content-Type':'application/json'}
            elif qry is not None and qry.posted_by != identity['username'] :
                return {'status': 'NOT FOUND','message':'Unautorized User'}, 404, {'Content-Type':'application/json'}
            else:    
                qry.item_name = args['item_name']
                qry.category = args['category']
                qry.price = args['price']
                qry.size = args['size']
                qry.color = args['color']
                qry.posted_by = identity['username']
                db.session.commit()

                return marshal(qry, Items.response_field), 200, {'Content-Type': 'application/json'}
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }
            
    @jwt_required
    def delete(self, item_id):
        user = get_jwt_identity()
        identity = marshal(user, Users.response_field)

        if identity['status'] == 'user':
            qry = Items.query.get(item_id)
            if qry is None:
                return {'status': 'NOT FOUND','message':'Item not found'}, 404, {'Content-Type':'application/json'}        
            elif qry is not None and qry.posted_by != identity['username'] :
                return {'status': 'NOT FOUND','message':'Unautorized User'}, 404, {'Content-Type':'application/json'}            
            else:
                db.session.delete(qry)
                db.session.commit()
                return ("Deleted")
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }

class ItemUserResource(Resource):
    @jwt_required
    def get(self, item_id=None):
        user = get_jwt_identity()
        identity = marshal(user, Users.response_field)
        if identity['status'] == 'user':
            if item_id == None:
                parse = reqparse.RequestParser()
                parse.add_argument('p',type=int,location='args',default=1)
                parse.add_argument('rp',type=int,location='args',default=5)
                parse.add_argument('item_name',location='args')
                parse.add_argument('max_price', type=int, location='args')
                parse.add_argument('category',location='args')
                parse.add_argument('size',location='args')
                parse.add_argument('color',location='args')
                parse.add_argument('posted_by',location='args')

                args = parse.parse_args()
                offset = args['p']*args['rp']-args['rp']
                qry = Items.query
                if args['item_name'] is not None:
                    qry = qry.filter(Items.item_name.like("%"+args['item_name']+"%"))               
                if args['category'] is not None:
                    qry = qry.filter(Items.category.like(args['category']))
                if args['size'] is not None:
                    qry = qry.filter(Items.size.like(args['size']))
                if args['color'] is not None:
                    qry = qry.filter(Items.color.like(args['color']))
                if args['posted_by'] is not None:
                    qry = qry.filter(Items.posted_by.like("%"+args['posted_by']+"%"))    
                item_lists = []
                for item_list in qry.limit(args['rp']).offset(offset).all():
                    if item_list.posted_by == identity['username'] :
                        item = marshal(item_list, Items.response_field)
                        if args['max_price'] is not None:
                            if item['price'] <= args['max_price'] :
                                item_lists.append(item)
                        else :
                            item_lists.append(item)
                return item_lists, 200, {'Content-Type': 'application/json'}
                        
            else:
                qry = Items.query.get(item_id)
                if qry is not None and qry.posted_by == identity['username']:
                    return marshal(qry, Items.response_field)
                return {'status': 'NOT FOUND','message':'Item not found'}, 404, {'Content-Type':'application/json'}
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }


api.add_resource(ItemResource,'/item', '/item/<int:item_id>')
api.add_resource(ItemUserResource,'/posted_item', '/posted_item/<int:item_id>')

