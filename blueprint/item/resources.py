import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_cors import CORS
from blueprint import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprint.user import Users
from . import *

bp_item = Blueprint('item', __name__)
api = Api(bp_item)
CORS(bp_item)
class ItemResource(Resource):
    def get(self, item_id=None):
        if item_id == None:
            parse = reqparse.RequestParser()
            parse.add_argument('item_name',location='args')
            parse.add_argument('max_price', type=int, location='args')
            parse.add_argument('category',location='args')
            parse.add_argument('size',location='args')
            parse.add_argument('color',location='args')
            parse.add_argument('posted_by',location='args')
          
            args = parse.parse_args()
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
            for item_list in qry:
                item = marshal(item_list, Items.response_field)
                if args['max_price'] is not None:
                    if item['price'] <= args['max_price'] :
                        item_lists.append(item)
                else :
                    item_lists.append(item)
            return {'status':'success','data':item_lists}, 200, {'Content-Type': 'application/json'}
        else:
            qry = Items.query.get(item_id)
            data = marshal(qry, Items.response_field)
            if qry is not None:
                return {'status':'success','data':data}, 200, {'Content-Type': 'application/json'}
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
            parse.add_argument('qty', location='json', type=int, required=True)
            parse.add_argument('description', location='json', required=True)
            parse.add_argument('imgurl1', location='json', required=True)
            parse.add_argument('imgurl2', location='json', required=True)
            parse.add_argument('imgurl3', location='json', required=True)
            parse.add_argument('imgurl4', location='json', required=True)

            args = parse.parse_args()

            items = Items(None, args['item_name'], args['category'], args['price'], args['size'], args['color'], args['qty'], identity['store_name'], args['description'], args['imgurl1'], args['imgurl2'], args['imgurl3'], args['imgurl4'])

            db.session.add(items)
            db.session.commit()
            data = marshal(items, Items.response_field)

            return {'status':'success', 'message':"item posted", 'data': data}, 200, {'Content-Type': 'application/json'}

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
            parse.add_argument('qty', location='json', type=int, required=True)
            parse.add_argument('description', location='json', required=True)
            parse.add_argument('imgurl1', location='json', required=True)
            parse.add_argument('imgurl2', location='json', required=True)
            parse.add_argument('imgurl3', location='json', required=True)
            parse.add_argument('imgurl4', location='json', required=True)
            args = parse.parse_args()

            qry = Items.query.get(item_id)
            if qry is None :
                return {'status': 'NOT FOUND','message':'Item not found'}, 404, {'Content-Type':'application/json'}
            elif qry is not None and qry.posted_by != identity['store_name'] :
                return {'status': 'NOT FOUND','message':'Unautorized User'}, 404, {'Content-Type':'application/json'}
            else:    
                qry.item_name = args['item_name']
                qry.category = args['category']
                qry.price = args['price']
                qry.size = args['size']
                qry.color = args['color']
                qry.qty = args['qty']
                qry.description = args['description']
                qry.imgurl1 = args['imgurl1']
                qry.imgurl2 = args['imgurl2']
                qry.imgurl3 = args['imgurl3']
                qry.imgurl4 = args['imgurl4']

                db.session.commit()
                data = marshal(qry, Items.response_field)

                return {'status':'success', 'message':"Items's data edited", 'data': data}, 200, {'Content-Type': 'application/json'}
        else:
            return {'status':'UNAUTORIZED', 'message':'unautorized user'}, 401, { 'Content-Type': 'application/json' }
            
    @jwt_required
    def delete(self, item_id):
        user = get_jwt_identity()
        identity = marshal(user, Users.response_field)

        if identity['status'] == 'user':
            qry = Items.query.get(item_id)
            if qry is None:
                return {'status': 'NOT FOUND','message':'Item not found'}, 404, {'Content-Type':'application/json'}        
            elif qry is not None and qry.posted_by != identity['store_name'] :
                return {'status': 'NOT FOUND','message':'Unautorized User'}, 404, {'Content-Type':'application/json'}            
            else:
                db.session.delete(qry)
                db.session.commit()
                data = marshal(qry, Items.response_field)
                return {'status': 'success','message':"Item's data deleted", 'data': data}, 200, {'Content-Type':'application/json'}        
        else:
            return {'status':'UNAUTORIZED', 'message':'unautorized user'}, 401, { 'Content-Type': 'application/json' }

class ItemUserResource(Resource):
    @jwt_required
    def get(self, item_id=None):
        user = get_jwt_identity()
        identity = marshal(user, Users.response_field)
        if identity['status'] == 'user':
            if item_id == None:
                parse = reqparse.RequestParser()
                parse.add_argument('item_name',location='args')
                parse.add_argument('max_price', type=int, location='args')
                parse.add_argument('category',location='args')
                parse.add_argument('size',location='args')
                parse.add_argument('color',location='args')
                parse.add_argument('posted_by',location='args')

                args = parse.parse_args()
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
                for item_list in qry:
                    if item_list.posted_by == identity['store_name'] :
                        item = marshal(item_list, Items.response_field)
                        if args['max_price'] is not None:
                            if item['price'] <= args['max_price'] :
                                item_lists.append(item)
                        else :
                            item_lists.append(item)
                return {'status':'success','data':item_lists}, 200, {'Content-Type': 'application/json'}
                        
            else:
                qry = Items.query.get(item_id)
                data = marshal(qry, Items.response_field)
                if qry is not None and qry.posted_by == identity['store_name']:
                    return {'status':'success','data':data}, 200, {'Content-Type': 'application/json'}
                return {'status': 'NOT FOUND','message':'Item not found'}, 404, {'Content-Type':'application/json'}
        else:
            return {'status':'UNAUTORIZED', 'message':'unautorized user'}, 401, { 'Content-Type': 'application/json' }


api.add_resource(ItemResource,'/item', '/item/<int:item_id>')
api.add_resource(ItemUserResource,'/posted_item', '/posted_item/<int:item_id>')

