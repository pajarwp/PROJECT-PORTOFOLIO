import random, logging
from blueprint import db
from flask_restful import fields

class Carts(db.Model):
    __tablename__ = "cart"
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyer_id = db.Column(db.Integer)
    item_id =  db.Column(db.Integer)
    item_sum = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    transaction_id = db.Column(db.Integer)

    response_field = {
        'cart_id' : fields.Integer,
        'buyer_id' : fields.Integer,
        'item_id' : fields.Integer,
        'item_sum' : fields.Integer,
        'total_price' : fields.Integer,
        'transaction_id' : fields.Integer,
    }

    def __init__(self, cart_id, buyer_id, item_id, item_sum, total_price, transaction_id):
        self.cart_id = cart_id
        self.buyer_id = buyer_id
        self.item_id = item_id
        self.item_sum = item_sum
        self.total_price = total_price
        self.transaction_id = transaction_id

    def __repr__(self):
        return '<Cart %d>' % self.cart_id
