import random, logging
from blueprint import db
from flask_restful import fields

class Transactions(db.Model):
    __tablename__ = "transaction"
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyer_id = db.Column(db.Integer)
    total_price = db.Column(db.Integer)

    response_field = {
        'transaction_id' : fields.Integer,
        'buyer_id' : fields.Integer,
        'total_price' : fields.Integer,
    }

    def __init__(self, transaction_id, buyer_id, total_price):
        self.transaction_id = transaction_id
        self.buyer_id = buyer_id
        self.total_price = total_price

    def __repr__(self):
        return '<Transaction %d>' % self.transaction_id
